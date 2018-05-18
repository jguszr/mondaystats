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
    page = 0
    lst_of_pulses = []
    while True:
        pulses = requests.get("https://api.monday.com:443/v1/boards/"+str(board_id)+"/pulses.json?page="+str(page)+"&per_page=25&order_by=updated_at_desc&api_key="+str(KEY_TOKEN))
        if len(pulses.content) != 2:
            lst_of_pulses.append(pulses.content)
        else:
            break
        page +=1

    return lst_of_pulses

        

def prepare_data():
    mb = get_board_by_name("MainBoard",get_all_boards())
    x = get_board_pulses(mb["id"])
    lst_of_boards = []
    for i in x:
        lst_of_boards.append(json.loads(i))

    lst = []
    for f in lst_of_boards:
        for d in f :
            rec = {}
            rec["name"] = d["pulse"]["name"]
            rec["created_at"] = d["pulse"]["created_at"]
            rec["updated_at"] = d["pulse"]["updated_at"]
            rec["group_id"] = d["board_meta"]["group_id"]
            ## handling column_values 
            rec["Assignee"] = None
            rec["Priority"] = None
            rec["Status"] = None
            rec["Estimado"] = None
            rec["Realizado"] = None
            rec["Plataformas"] = None

            for c in d["column_values"]:
                try:
                    if rec["Assignee"] == None:
                        rec["Assignee"] = handle_internal_value(c, "Assignee", "name")
                    if rec["Priority"] == None:
                        rec["Priority"] = handle_internal_value(c, "Priority", "index")
                    if rec["Status"] == None:
                        rec["Status"] = handle_internal_value(c, "Status", "index")
                    if rec["Estimado"] == None:
                        rec["Estimado"] = handle_internal_value(c, "Estimado", "")
                    if rec["Realizado"] == None:
                        rec["Realizado"] = handle_internal_value(c, "Realizado", "")
                    if rec["Plataformas"] == None:
                        rec["Plataformas"] = handle_internal_value(c, "Plataformas", "")
                    print(rec)
                except:
                    continue
            
            lst.append(rec)

    return pd.DataFrame(lst)

def handle_internal_value(c, required_title, returning_field):
    if c["title"]==required_title:
        if returning_field=="":
            return c["value"]
        else:
            try:
                return c["value"][returning_field]
            except:
                raise

def handle_ds(data):
    data["Estimado"] = pd.to_numeric(data["Estimado"]) 
    data["Realizado"] = pd.to_numeric(data["Realizado"]) 

    return data

 
ds = handle_ds(prepare_data())
#print(ds.head(20))