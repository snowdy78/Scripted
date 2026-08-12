import mysql.connector
import hashlib
import datetime
import typing
from ParseTypes import ParseResponseData, Script, Topic, Subtopic

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
        script: Script = {
            "url": db_script['url'],
            "topic": db_script['topic'],
            "subtopic": db_script['subtopic'],
            "content": db_script['content'], 
            "date_parsed": db_script['date_parsed']
        }
        return script

    @staticmethod
    def _asSubtopic(db_subtopic) -> Subtopic:
        subtopic: Subtopic = {
            "name": db_subtopic['subtopic'],
            "topic": db_subtopic['topic']
        }
        return subtopic
    @staticmethod
    def _applyFilters(query: str, filters: list[str]) -> str:
        return query.join(" WHERE ".join(i.join(" ") for i in filters))

    def insertScriptData(self, script_data: Script):
        script_data['topic'] = script_data['topic'].upper()
        script_data['subtopic'] = script_data['subtopic'] if not script_data['subtopic'] else script_data['subtopic'].upper()
        print(f"Inserting script data: {script_data.values()}")
        self.cursor.execute(
            "INSERT INTO scripts (url, topic, subtopic, content, date_parsed) VALUES (%s, %s, %s, %s, %s)",
            (script_data['url'], script_data['topic'], script_data['subtopic'], script_data['content'], script_data['date_parsed'], )
        )
        self.db.commit()

    def getScriptData(self, url: str) -> Script:
        self.cursor.execute("SELECT * FROM scripts WHERE url = %s", (hashUrl(url),))
        db_script = self.cursor.fetchone()
        script: Script = self._asScript(db_script)
        return script

    def insertTopic(self, topic: Topic):
        if None in topic['subtopics'] or "" in topic['subtopics']:
            raise ValueError("Subtopic is NoneType")
        self.cursor.executemany(
            "INSERT IGNORE INTO subtopics (name, topic) VALUES (DEFAULT, %s, %s)", tuple((
                (sub_name, topic['name']) for sub_name in topic['subtopics']
            ))
        )
        self.cursor.executemany(
            "INSERT INTO topics (id, name, subtopic) VALUES (DEFAULT, %s, %s) ON DUPLICATE KEY UPDATE datetime", 
            tuple(((topic['name'], sub_name) for sub_name in topic['subtopics']))
        )
        self.db.commit()

    def getScripts(self, filters: list[str]) -> list[Script]:
        scripts = []
        result = self.cursor.execute(self._applyFilters("SELECT * FROM scripts", filters))
        if result is None:
            raise ValueError("Result is NoneType")
        for row in result:
            scripts.append(self._asScript(row))
        return scripts

    def getTopics(self, filters: list) -> list[Topic]:
        topics = []
        result = self.cursor.execute(self._applyFilters("SELECT * FROM topics", filters))
        if result is None:
            raise ValueError("Result is NoneType")
        for row in result:
            topics.append(self._asTopic(row))
        return topics

    def close(self):
        self.cursor.close()
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()