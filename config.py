from Scripted.Database import Database

_database: Database | None = None

def initDatabase(db: Database | None = None) -> None:
    # pylint: disable=global-statement
    global _database
    _database = db or Database()
    print("initialize DB")

def useDatabase() -> Database:
    # pylint: disable=global-statement
    if _database is None:
        raise ValueError("Database is not initialized. (please reconnect)")
    return _database

def closeDatabase() -> None:
    # pylint: disable=global-statement
    if isinstance(_database, Database):
        _database.close()
        print("close DB")
