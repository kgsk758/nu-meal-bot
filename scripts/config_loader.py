import os
from dotenv import load_dotenv
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
from config import constants as const

class Config:
    def __init__(self):
        load_dotenv("../.env") 

        self.ck = os.environ.get('ck')
        self.cs = os.environ.get('cs')
        self.at = os.environ.get('at')
        self.ats = os.environ.get('ats')

        self.HOKUBU_ID = const.HOKUBU_ID
        self.FOREST_ID = const.FOREST_ID
        self.MEIDINING_ID = const.MEIDINING_ID
        self.SAI_ID = const.SAI_ID
        self.IGAKUBU_ID = const.IGAKUBU_ID

        self.SCHEDULE_URL = const.SCHEDULE_URL