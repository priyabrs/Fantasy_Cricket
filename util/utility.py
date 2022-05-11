from contextlib import contextmanager

@contextmanager
def connect_db(database):
    try:
        database.connect()
        yield database
    finally:
        database.close()


class DatabaseOperations():

    def __init__(self, db) -> None:
        self.db = db

    def create_tables(self, table_list):
        with connect_db(self.db) as dbConnect:
            dbConnect.create_tables(table_list)