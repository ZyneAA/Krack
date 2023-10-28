import requests, json

class SteamDetail():
    def __init__(self, id: int, region: str, lang: str):
        self.id = id
        self. region = region
        self.lang = lang
    
    def steam_detail(self):
        url = f"https://store.steampowered.com/api/appdetails/?appids={self.id}&cc={self.region}&l={self.lang}"
        response = requests.get(url)
        data = json.loads(response.text)
        with open("detail.json", "w") as f:
            json.dump(data, f, indent = 4)   
     
#steam_detail(1245620)
detail1 = SteamDetail(570, "US", "en")
detail1.steam_detail()
