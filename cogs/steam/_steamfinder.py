import sqlite3

def findgame(n):
    connection = sqlite3.connect("steam.db")
    db = connection.cursor()
    db.execute("SELECT appid, name FROM steam_data")
    results = db.fetchall()
    for row in results:
        if n.lower() in row[1].lower():
            print(str(row[0]) + " " + str(row[1]))

findgame("hogwART")