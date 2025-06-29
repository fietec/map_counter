from flask import Flask, request
import os
import json

app = Flask(__name__)

DIR:str = os.path.join(os.getcwd(), "")
MAPS_PATH:str = os.path.join(DIR, "maps.json")
POST_SUCCESS = {"success" : True}

def get_data(path:str) -> list:
    with open(path, "r") as f:
        return json.loads(f.read())

def write_data(path:str, data:list):
    with open(path, "w") as f:
        f.write(json.dumps(data))

def post_error(message:str) -> dict:
    return {"success" : False, "message": message}
    
def get_file(path:str):
    with open(os.path.join(DIR, path), "rb") as f:
        return f.read()

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return get_file("maps.html")
    else:
        args = request.json
        if "map" not in args:
            return post_error("No action provided!")
        map = args["map"]
        season_name = args["season"]
        data = get_data(MAPS_PATH)
        if season_name == None:
            season = data[next(iter(data))]
        elif season_name in data:
            season = data[season_name]
        else:
            return post_error("Invalid season name")
        maps = season["maps"]
        if map not in maps:
            return post_error("Unknown map!")
        t_played = data[season_name]["maps"][map]["played"] + args["change"]
        if t_played < 0:
            t_played = 0
        data[season_name]["maps"][map]["played"] = t_played
        write_data(MAPS_PATH, data)
        return POST_SUCCESS
        
@app.route('/reset', methods=['POST'])
def reset():
    if request.method == 'POST':
        args = request.json
        if "season" not in args:
            return post_error("No season provided!")
        season_name = args["season"]
        data = get_data(MAPS_PATH)
        if season_name == None:
            season = data[next(iter(data))]
        elif season_name in data:
            season = data[season_name]
        else:
            return post_error("Invalid season name")
        maps = data[season_name]["maps"]
        for map in maps:
            data[season_name]["maps"][map]["played"] = 0
        write_data(MAPS_PATH, data)
        return POST_SUCCESS
    return post_error("Invalid method")
    
@app.route('/maps', methods=['POST'])
def maps():
    if request.method != 'POST': return post_error("Invalid method")
    args = request.json
    if "season" not in args:
        return post_error("No season provided!")
    season_name = args["season"]
    data = get_data(MAPS_PATH)
    if season_name == None:
        season = data[next(iter(data))]
    elif season_name in data:
        season = data[season_name]
    else:
        return post_error("Invalid season name")
    maps = season["maps"]
    ret = {"success": True, "maps": maps, "total": sum([maps[map]["played"] for map in maps]), "seasons": [{"value": key, "name": data[key]["name"]} for key in data.keys()], "period": {"from": season["date-from"], "until": season["date-to"]}}
    print(ret)
    return ret
    
app.run()