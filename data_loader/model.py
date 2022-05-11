from email.policy import default
from peewee import SqliteDatabase, Model, TextField, DateField, IntegerField, CharField
# from sqlalchemy import null
import datetime
import os

DB_PATH = os.path.abspath('database')
matchdata_db = SqliteDatabase(os.path.join(DB_PATH, 'matchdata.db'))

class BaseTable(Model):

    created_at = DateField(default=datetime.datetime.now)
    updated_at = DateField(default=datetime.datetime.now)
    class Meta:
        database = matchdata_db

class MatchInfo(BaseTable):
    match_id = IntegerField(null=False, primary_key=True)
    match_date = DateField(null=False)
    season = CharField(max_length=20)
    venue = TextField()
    winning_team = TextField()
    loosing_team = TextField()
    motm = TextField()
    match_result = CharField(max_length=20)

# class BattingStats(BaseTables):

# if __name__ == '__main__':
#     print(os.path.join(DB_PATH, 'matchdata.db'))
