import asyncio, sqlite3, csv, re, requests, json

class ADB():
    def __init__(self):
        self.arr = {}
        self.connection = sqlite3.connect("steam.db")
        self.db = self.connection.cursor()
        self.s = self.db.execute("SELECT * FROM steam_data")
        self.data = self.s.fetchall()
        self.a()
        
    async def add(self):
        for i in self.data:
            await asyncio.sleep(0.01)
            yield i[0]
            
    async def cr(self):
        async for i in self.add():
            await asyncio.sleep(0.01)
            print(i)
    
    def a(self):
        for i in self.data:
            self.arr.__setitem__(i[0], i[1])
    
    def csv_reder(self, name, item):
        pattern = re.compile(item, re.IGNORECASE)
        with open(name, "r") as f:
            reader = csv.reader(f)  
            for i in reader:  
                match = pattern.search(i[0])
                if match:
                    print(i)
                    
    def direct_search(self, name):
        pattern = re.compile(name, re.IGNORECASE)
        applist = "http://api.steampowered.com/ISteamApps/GetAppList/v0002"
        response = requests.get(applist)
        data = json.loads(response.text)
        for i in data:
            lol = data[i]
            for j in lol:
                for k in lol[j]:
                    match = pattern.search(k["name"])
                    if match:
                        print(k)
        
a = ADB()
print(a.direct_search("forza horizon 5"))