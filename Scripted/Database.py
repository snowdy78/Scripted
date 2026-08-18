import typing
import hashlib
import mysql.connector
from Scripted.ParseTypes import Script, Topic, Subtopic
from Scripted.Settings import Settings


def hashUrl(url: str):
    return hashlib.sha1(url.encode("utf-8")).hexdigest()

class Database:
    def __init__(self, host, port, user, password, name_database):
        self.db = mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database=name_database,
        )
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `topics` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `subtopics` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                topic_id INT NOT NULL,
                name  TEXT NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `scripts` (
                url VARCHAR(500) PRIMARY KEY,
                topic_id INT NOT NULL,
                subtopic_id INT NULL,
                content LONGTEXT NULL,
                date_parsed DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (subtopic_id) REFERENCES subtopics (id) ON DELETE SET NULL ON UPDATE CASCADE
            );
        """)
        self.db.commit()
        print("Database initialized!")

    @staticmethod
    def _asScript(db_script) -> Script:
        return Script(
            db_script[0],
            db_script[1],
            db_script[2],
            db_script[3],
            db_script[4]
        )

    @staticmethod
    def _asSubtopic(db_subtopic) -> Subtopic:
        return Subtopic(
            db_subtopic[0],
            db_subtopic[1],
            db_subtopic[2]
        )

    @staticmethod
    def _asTopic(db_topic) -> Topic:
        return Topic(
            db_topic[0],
            db_topic[1]
        )

    @staticmethod
    def _applyFilters(query: str, filters: list[str]) -> str:
        if not filters:
            return query
        where_clause = " AND ".join(filters)
        return f"{query} WHERE {where_clause}"

    def _get(
        self,
        table_name: str,
        filters: list[str],
        data: tuple[typing.Any],
        castFunc: typing.Callable
    ):
        query = self._applyFilters(f"SELECT * FROM {table_name}", filters)
        self.cursor.execute(
            query,
            data
        )
        rows = self.cursor.fetchall()
        if rows is None:
            raise ValueError("Result is NoneType")
        return list(castFunc(row) for row in rows)

    def _getIdIfNotExists(
        self,
        table_name: str,
        name: str | int | None,
        insertFunc: typing.Callable[[str], None],
        castFunc: typing.Callable,
        getIdFunc: typing.Callable[[typing.Any], str] = lambda x: str(x.id)
    ) -> str | None:
        if name is None:
            return None
        if isinstance(name, int):
            return str(name)
        if not isinstance(name, str):
            raise TypeError(f"Expected str/int/None, got {type(name)}")
        result = self._get(table_name, ['name=%s'], (name, ), castFunc)
        if not result:
            insertFunc(name)
        return getIdFunc(self._get(table_name, ['name=%s'], (name, ), castFunc)[0])

    def getTopicIdIfNotExists(
        self,
        name: str | int | None
    ) -> str | None:
        return self._getIdIfNotExists(
            "topics",
            name,
            self.insertTopic,
            self._asTopic
        )

    def getSubtopicIdIfNotExists(
        self,
        name: str | int | None,
        topic_id: str
    ) -> str | None:
        return self._getIdIfNotExists(
            "subtopics",
            name,
            lambda name: self.insertSubtopic(name, topic_id),
            self._asSubtopic
        )

    def insertScriptData(
        self,
        url: str,
        topic: int | str,
        subtopic: int | str | None,
        content: str = ""
    ):
        print("Inserting script data...")
        topic_id: str | None = self.getTopicIdIfNotExists(topic)
        if not topic_id:
            raise ValueError(f"Topic id is None ({topic_id})")
        subtopic_id: str | None = self.getSubtopicIdIfNotExists(subtopic, topic_id)
        self.cursor.execute(
            """INSERT INTO scripts 
            (url, topic_id, subtopic_id, content, date_parsed) 
            VALUES (%s, %s, %s, %s, DEFAULT) AS item ON DUPLICATE KEY UPDATE 
            date_parsed = DEFAULT, content = item.content""",
            (
                url,
                topic_id,
                subtopic_id,
                content
            )
        )
        self.db.commit()
        print("Inserting done!")

    def insertTopic(self, name: str):
        self.cursor.execute(
            """INSERT INTO topics (id, name) VALUES 
            (DEFAULT, %s) AS item ON DUPLICATE KEY UPDATE name = item.name""",
            (name, )
        )
        self.db.commit()

    def insertSubtopic(self, name: str, topic: int | str):
        topic_id: str | None = self.getTopicIdIfNotExists(topic)
        if not topic_id:
            raise ValueError(f"Topic id is None ({topic_id})")
        self.cursor.execute(
            """INSERT INTO subtopics (id, topic_id, name) VALUES 
            (DEFAULT, %s, %s) AS item ON DUPLICATE KEY UPDATE name = item.name""",
            (topic_id, name)
        )
        self.db.commit()

    def getScripts(self, filters: list[str], data: tuple[typing.Any, ...]) -> list[Script]:
        return self._get("scripts", filters, data, self._asScript)

    def getTopics(self, filters: list[str], data: tuple[typing.Any, ...]) -> list[Topic]:
        return self._get("topics", filters, data, self._asTopic)

    def getSubtopics(
        self,filters: list[str],
        data: tuple[typing.Any, ...]
    ) -> list[Subtopic]:
        return self._get("subtopic", filters, data, self._asSubtopic)

    def close(self):
        self.cursor.close()
        self.db.close()
        print("Database connection closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

class DatabaseLocalConfiguration(Database):
    def __init__(self):
        local_config = Settings.get()["settings"]["database"]
        host = local_config["host"]
        port = local_config["port"]
        user = local_config["user"]
        password = local_config["password"]
        name_database = local_config["database"]
        super().__init__(host, port, user, password, name_database)

database = DatabaseLocalConfiguration()
