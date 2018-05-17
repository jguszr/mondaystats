## getting stuff from Monday

import requests 
from requests.auth import HTTPBasicAuth
import json
import objectpath

global KEY_TOKEN
KEY_TOKEN = "2494b9d018b6e9699f352d72f3c0fd76"

def get_all_boards():
    print("get_boards")
    boards = requests.get("https://api.monday.com:443/v1/boards.json?per_page=12&only_globals=true&order_by_latest=false&api_key="+ str(KEY_TOKEN))
    return json.loads(boards.content)

def get_board_by_name(board_name, jsoncontent):
    print("get_board_by_name(board_name, jsoncontent):")
    for board in jsoncontent:
        if board["name"]==board_name:
            return board
    return None

def get_board_pulses(board_id):
    print("get_board_pulses(board_id):")
    pulses = requests.get("https://api.monday.com:443/v1/boards/"+str(board_id)+"/pulses.json?per_page=25&api_key="+str(KEY_TOKEN))
    return json.loads(pulses.content)