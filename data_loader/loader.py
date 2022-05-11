from pathlib import Path
import os, errno
import json
import sys
from unittest import result
import requests, zipfile, io
from datetime import datetime
from model import matchdata_db, MatchInfo

sys.path.append(r'..\fantasy_cricket')

from util.utility import connect_db

DATALOAD_URL = 'https://cricsheet.org/downloads/ipl_json.zip'
DATA_FILE_PATH = 'C:/Users/Priyabrata/Desktop/Python/VS Code/fantasy_cricket/data/'

class Loader():
    
    def __init__(self):
        pass

    def silent_remove(self, filename):
        try:
            os.remove(filename)
        except OSError as e: # this would be "except OSError, e:" before Python 2.6
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred

    def update_data_files(self, file_id=None):
        req = requests.get(DATALOAD_URL)
        z = zipfile.ZipFile(io.BytesIO(req.content))
        if file_id:
            file_id += 1
            z.extract(member=f'{file_id}.json', path=DATA_FILE_PATH)
        else:
            z.extractall(DATA_FILE_PATH)

    def get_match_file_id(self, match_file_id = 'latest'):
        if match_file_id == 'latest':
            file_list =  os.listdir(DATA_FILE_PATH)
            file_list.remove('README.txt')
            file_id_list = sorted([int(file_id[:-5]) for file_id in file_list], reverse=True)
            file_id = file_id_list[0]
        return file_id


    def load_match_info_to_db(self, file):
        try:
            with open(f'data/{file}') as json_file:
                match_data = json.load(json_file)
            match_id = int(file[:-5])
            match_info = match_data['info']
            match_date = datetime.strptime(match_info['dates'][0], '%Y-%m-%d').date()
            season = match_info['season']
            venue = match_info['venue']
            
            if 'winner' not in match_info['outcome'].keys():
                if match_info['outcome']['result'] == 'tie':
                    winning_team = match_info['outcome']['eliminator']
                    motm = match_info['player_of_match'][0]
                    match_result = 'tie'
                else:
                    winning_team = match_info['teams'][0]
                    match_result = match_info['outcome']['result']
                    motm = 'NA'
            else:        
                winning_team = match_info['outcome']['winner']
                match_result = 'normal'
                motm = match_info['player_of_match'][0]
            loosing_team = [team for team in match_info['teams'] if team != winning_team][0]
            
            with connect_db(matchdata_db) as dbConnect:
                MatchInfo.create(
                    match_id = match_id,
                    match_date = match_date,
                    season = season,
                    venue = venue,
                    winning_team = winning_team,
                    loosing_team = loosing_team,
                    motm = motm,
                    match_result = match_result
                )
        except Exception as e:
            print(e)

if __name__ == '__main__':
    l = Loader()
    # l.load_match_info_to_db('1304073.json')
    file_list =  os.listdir(DATA_FILE_PATH)
    file_list.remove('README.txt')
    for file in file_list:
        l.load_match_info_to_db(file)
