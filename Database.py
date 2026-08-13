import hashlib
import mysql.connector
from typing import Callable
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
        return {
            "url": db_script['url'],
            "topic_id": db_script['topic_id'],
            "subtopic_id": db_script['subtopic_id'],
            "content": db_script['content'], 
            "date_parsed": db_script['date_parsed']
        }

    @staticmethod
    def _asSubtopic(db_subtopic) -> Subtopic:
        return {
            "id": db_subtopic['id'],
            "name": db_subtopic['name'],
            "topic_id": db_subtopic['topic_id']
        }

    @staticmethod
    def _asTopic(db_topic) -> Topic:
        return {
            "id": db_topic['id'],
            "name": db_topic['name']
        }

    @staticmethod
    def _applyFilters(query: str, filters: list[str]) -> str:
        return query.join(" WHERE ".join(i.join(" ") for i in filters))

    def _get(self, table_name: str, filters: list[str], func: Callable):
        result = self.cursor.execute(
            self._applyFilters("SELECT * FROM ".join(table_name), filters)
        )
        if result is None:
            raise ValueError("Result is NoneType")
        return list(func(row) for row in result)
    def insertScriptData(self, script_data: Script):
        script_data['topic_id'] = script_data['topic_id'].upper()
        subtopic = script_data['subtopic_id']
        script_data['subtopic_id'] = subtopic if not subtopic else subtopic.upper()
        print(f"Inserting script data: {script_data.values()}")
        self.cursor.execute(
            """INSERT INTO scripts (url, topic_id, subtopic_id, content, date_parsed) 
            VALUES (%s, %s, %s, %s, %s)""",
            (
                script_data['url'],
                script_data['topic'],
                script_data['subtopic'],
                script_data['content'],
                script_data['date_parsed'],
            )
        )
        self.db.commit()

    def insertTopic(self, topic: Topic):
        self.cursor.executemany(
            """INSERT INTO topics (id, name) VALUES 
            (DEFAULT, %s) ON DUPLICATE KEY UPDATE datetime""",
            topic['id']
        )
        self.db.commit()

    def getScripts(self, filters: list[str]) -> list[Script]:
        return self._get("scripts", filters, self._asScript)

    def getTopics(self, filters: list) -> list[Topic]:
        return self._get("topics", filters, self._asTopic)

    def getSubtopics(self, filters: list) -> list[Subtopic]:
        return self._get("subtopic", filters, self._asSubtopic)

    def close(self):
        self.cursor.close()
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()