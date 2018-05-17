## getting stuff from Monday

import requests 
from requests.auth import HTTPBasicAuth
import json
import objectpath
import pandas as pd

global KEY_TOKEN
KEY_TOKEN = "2494b9d018b6e9699f352d72f3c0fd76"

def get_all_boards():
    print("get_boards")
    boards = requests.get("https://api.monday.com:443/v1/boards.json?per_page=12&only_globals=true&order_by_latest=false&api_key="+ str(KEY_TOKEN))
    return json.loads(boards.content)

def get_board_by_name(board_name, json_content):
    print("get_board_by_name(board_name, jsonc_ontent):")
    for board in json_content:
        if board["name"]==board_name:
            return board
    return None

def get_board_pulses(board_id):
    print("get_board_pulses(board_id):")
    pulses = requests.get("https://api.monday.com:443/v1/boards/"+str(board_id)+"/pulses.json?per_page=25&api_key="+str(KEY_TOKEN))
    return pulses.content

def build_dataset(json_content):
    return pd.read_json(json_content)

def test_integration():
    mb = get_board_by_name("MainBoard",get_all_boards())
    x = get_board_pulses(mb["id"])
    f = json.loads(x)
    print(type(f))
    #print(f)
    print(type(f[1]))
    lst = []
    for d in f :
        rec = {}
        rec["name"] = d["pulse"]["name"]
        rec["created_at"] = d["pulse"]["created_at"]
        rec["updated_at"] = d["pulse"]["updated_at"]
        rec["group_id"] = d["board_meta"]["group_id"]
        ## handling column_values 
        for c in d["column_values"]:
            try:
                rec["Assignee"] = handle_internal_value(c, "Assignee", "name")
                rec["Priority"] = handle_internal_value(c, "Priority", "index")
                rec["Status"] = handle_internal_value(c, "Status", "index")
                rec["Estimado"] = handle_internal_value(c, "Estimado", "")
                rec["Realizado"] = handle_internal_value(c, "Realizado", "")
                rec["Plataformas"] = handle_internal_value(c, "Plataformas", "")
            except:
                continue
        lst.append(rec)
    return lst

def handle_internal_value(c, required_title, returning_field):
    if c["title"]==required_title:
        if returning_field=="":
            return c["value"]
        else:
            try:
                return c["value"][returning_field]
            except:
                raise
        
    

print(test_integration())