from data_loader.model import matchdata_db, MatchInfo
from util.utility import DatabaseOperations, connect_db

if __name__ == '__main__':
    dbo = DatabaseOperations(matchdata_db)
    dbo.create_tables(table_list=[MatchInfo])
    # with connect_db(matchdata_db) as dbConnect:
    #     MatchDate.delete().where(MatchDate.match_id == 335982)

    # rec = MatchDate.delete().where(MatchDate.match_id == 335982)
    # rec.execute()
    # rec= MatchDate.get(match_id = 335982)
    # rec.delete_instance()
# from email.policy import default
# from peewee import SqliteDatabase, Model, TextField, DateField, IntegerField
# # from sqlalchemy import null
# import datetime
# import os

# # matchdata_db = SqliteDatabase('database\matchdata.db')

# path = os.path.abspath('database')
# print(os.path.join(path, 'matchdata.db'))
# matchdata_db = SqliteDatabase(os.path.join(path, 'matchdata.db'))

# matchdata_db.connect()