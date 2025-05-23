from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

MAPS_PATH:str = os.path.join(os.getcwd(), "./maps.json")
POST_SUCCESS = {"success" : True}

def get_data(path:str) -> list:
    with open(path, "r") as f:
        return json.loads(f.read())

def write_data(path:str, data:list):
    with open(path, "w") as f:
        f.write(json.dumps(data))

def post_error(message:str) -> dict:
    return {"success" : False, "message": message}

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("maps.html", maps=get_data(MAPS_PATH))
    else:
        data = request.json
        if "map" not in data:
            return post_error("No action provided!")
        map = data["map"]
        maps = get_data(MAPS_PATH)
        if map not in maps:
            return post_error("Unknown map!")
        t_played = maps[map]["played"] + data["change"]
        if t_played < 0:
            t_played = 0
        maps[map]["played"] = t_played
        write_data(MAPS_PATH, maps)
        return POST_SUCCESS
        
@app.route('/reset', methods=['POST'])
def reset():
    if request.method == 'POST':
        maps = get_data(MAPS_PATH)
        for map in maps:
            maps[map]["played"] = 0
        write_data(MAPS_PATH, maps)
        return POST_SUCCESS
    return post_error("Invalid method")
    
@app.route('/maps', methods=['GET'])
def maps():
    if request.method != 'GET': return post_error("Invalid method")
    maps = get_data(MAPS_PATH)
    return {"success": True, "maps": maps, "total": sum([maps[map]["played"] for map in maps])}
    
app.run()