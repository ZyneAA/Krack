import json, requests, csv

def steam_data():
    # connection = sqlite3.connect("steam.db")
    # db = connection.cursor()
    # db.execute("CREATE TABLE IF NOT EXISTS steam_data(appid INT, name TEXT)")

    applist = "http://api.steampowered.com/ISteamApps/GetAppList/v0002"
    response = requests.get(applist)
    data = json.loads(response.text)
    x = []
    d = []
    for i in data:
        lol = data[i]
        for j in lol:
            for k in lol[j]:
                tp = (k["name"], k["appid"])
                x.append(tp)
                d.append({"name": k["name"].upper(), "appid": k["appid"]})
    with open('cogs/steam/file.csv', 'w', encoding = 'utf-8', newline='') as file: 
        fields = ["name", "appid"]
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writerows(d)

    # db.execute("DELETE FROM steam_data")
    # db.executemany("INSERT INTO steam_data VALUES (?, ?)", x)
    # connection.commit()
    # db.close()
    print("ID updated!")

steam_data()