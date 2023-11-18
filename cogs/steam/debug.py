import json

with open("./detail_debug.json", 'r') as json_file:
    data = json.load(json_file)

    print(data["1568590"])