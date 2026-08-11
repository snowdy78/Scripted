import sqlite3
import hashlib
import datetime
from ParseTypes import ParseResponseData

class Database:
    class ScriptData:
        def __init__(self, response: ParseResponseData):
            if not response.params.url:
                raise ValueError("Error: params.url is None")
            if not response.content:
                raise ValueError("Error: can't create ScriptData by None")
            self.url_sha1 = hashlib.sha1(response.params.url.encode("utf-8")).hexdigest()
            self.content = response.content
            self.date_parsed = response.date_parsed or datetime.datetime.now()
        def values(self):
            return (self.url_sha1, self.content, self.date_parsed)

    def __init__(self):
        self.db = sqlite3.connect("database.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scripts (
                url_sha1 TEXT PRIMARY KEY,
                content TEXT
                date_parsed DATETIME
            )
            """
        )
        
        self.db.commit()

    def insertScriptData(self, script_data: ScriptData):
        print(f"Inserting script data: {script_data.values()}")
        self.cursor.execute(
            "INSERT INTO scripts (url_sha1, content, date_parsed) VALUES (?, ?, ?)",
            script_data.values()
        )
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()