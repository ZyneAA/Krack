import csv

def findgame(name):
    # connection = sqlite3.connect("steam.db")
    # db = connection.cursor()
    # db.execute("SELECT appid, name FROM steam_data")
    # results = db.fetchall()

    sar = str(name).upper()
    with open('./file.csv', "r", encoding = 'utf-8') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            upper = row[0].upper()
            if sar in upper:
                print(upper)

findgame("Assassin's Creed")