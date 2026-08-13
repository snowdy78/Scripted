import datetime
import typing
import hashlib
import mysql.connector
from ParseTypes import Script, Topic, Subtopic

def hashUrl(url: str):
    return hashlib.sha1(url.encode("utf-8")).hexdigest()


class Database:
    HOST = "localhost"
    USER = "root"
    PASSWORD = ""
    DATABASE = "scripted"
    def __init__(self):
        self.db = mysql.connector.connect(
            host = self.HOST,
            user = self.USER,
            password = self.PASSWORD,
            database = self.DATABASE
        )
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name TEXT NOT NULL
            )
            CREATE TABLE IF NOT EXISTS subtopics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                topic_id INT NOT NULL,
                name  VARCHAR(255) NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE ON UPDATE CASCADE
            )
            CREATE TABLE IF NOT EXISTS scripts (
                url VARCHAR(500) PRIMARY KEY,
                topic_id INT NOT NULL,
                subtopic_id INT NULL,
                content TEXT NULL,
                date_parsed DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (subtopic) REFERENCES subtopics (name) ON DELETE CASCADE ON UPDATE CASCADE NULL,
            )
            
            """
        )
        self.db.commit()

    @staticmethod
    def _asScript(db_script) -> Script:
        return Script(
            db_script['url'],
            db_script['topic_id'],
            db_script['subtopic_id'],
            db_script['content'], 
            db_script['date_parsed']
        )

    @staticmethod
    def _asSubtopic(db_subtopic) -> Subtopic:
        return Subtopic(
            db_subtopic['id'],
            db_subtopic['name'],
            db_subtopic['topic_id']
        )

    @staticmethod
    def _asTopic(db_topic) -> Topic:
        return Topic(
            db_topic['id'],
            db_topic['name']
        )

    @staticmethod
    def _applyFilters(query: str, filters: list[str]) -> str:
        return query.join(" WHERE ".join(i.join(" ") for i in filters))

    def _get(
        self,
        table_name: str,
        filters: list[str],
        data: tuple[typing.Any],
        castFunc: typing.Callable
    ):
        result = self.cursor.execute(
            self._applyFilters("SELECT * FROM ".join(table_name), filters),
            data
        )
        if result is None:
            raise ValueError("Result is NoneType")
        return list(castFunc(row) for row in result)

    def _getIdIfNotExists(
        self,
        table_name: str,
        name: str | int | None,
        insertFunc: typing.Callable[[str], None],
        castFunc: typing.Callable,
        getIdFunc: typing.Callable[[typing.Any], str] = lambda x: str(x.id)
    ) -> str:
        if name is None:
            return "NULL"
        if name is int:
            return str(name)
        if name is not str:
            raise TypeError(f"Expected str/int/None, got {type(name)}")
        insertFunc(name)
        return getIdFunc(self._get(table_name, ['name=%s'], (name, ), castFunc)[0])

    def getTopicIdIfNotExists(
        self,
        name: str | int | None
    ) -> str:
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
    ) -> str:
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
        content: str = "",
        date_parsed: datetime.datetime = datetime.datetime.now()
    ):
        topic_id: str = self.getTopicIdIfNotExists(topic)
        print("Inserting script data...")
        subtopic_id: str = self.getSubtopicIdIfNotExists(subtopic, topic_id)
        self.cursor.execute(
            """INSERT IGNORE INTO scripts 
            (url, topic_id, subtopic_id, content, date_parsed) 
            VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
            date_parsed = VALUES(date_parsed), content = VALUES(content)""",
            (
                url,
                topic_id,
                subtopic_id or "NULL",
                content,
                date_parsed,
            )
        )
        self.db.commit()

    def insertTopic(self, name: str):
        self.cursor.execute(
            """INSERT INTO topics (id, name) VALUES 
            (DEFAULT, %s)""",
            (name)
        )
        self.db.commit()

    def insertSubtopic(self, name: str, topic: int | str):
        topic_id: str = self.getTopicIdIfNotExists(topic)
        self.cursor.execute(
            """INSERT INTO subtopics (id, topic_id, name) VALUES 
            (DEFAULT, %s, %s)""",
            (topic_id, name)
        )
        self.db.commit()

    def getScripts(self, filters: list[str], data: tuple[typing.Any]) -> list[Script]:
        return self._get("scripts", filters, data, self._asScript)

    def getTopics(self, filters: list[str], data: tuple[typing.Any]) -> list[Topic]:
        return self._get("topics", filters, data, self._asTopic)

    def getSubtopics(
        self,filters: list[str],
        data: tuple[typing.Any]
    ) -> list[Subtopic]:
        return self._get("subtopic", filters, data, self._asSubtopic)

    def close(self):
        self.cursor.close()
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
