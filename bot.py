import os, asyncio, discord, json, requests, sqlite3, csv, re
from discord.ext import commands
from discord.ui import Button
import yt_dlp as youtube_dl
from cogs.steam import _steam

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
queues = {}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("🤡"))
    print("Initialized bot!")

class MyButton(discord.ui.View):
    def __init__(self, name, id, region):
        super().__init__()
        self.name = name
        self.id = id
        self.region = region

    @discord.ui.button(label="GetDetail(US)", style=discord.ButtonStyle.green, custom_id="button_us")
    async def us_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_game_details(interaction, self.region)

    @discord.ui.button(label="GetDetail(ARS)", style=discord.ButtonStyle.green, custom_id="button_ars")
    async def ars_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_game_details(interaction, "ar")

    async def send_game_details(self, interaction, region):
        url = f"https://store.steampowered.com/api/appdetails/?appids={self.id}&cc={region}&l=en"
        response = requests.get(url)
        data = json.loads(response.text)
        
        if data[self.id]["success"] == True:
            if not "price_overview" in data[self.id]['data']:
                embed = discord.Embed(title="Sorry 😶‍🌫️", description=f"The data regarding {self.name} could not be found")
                await interaction.response.edit_message(embed=embed , view=self)
            formatted_des = re.sub("<.*?>", "", data[self.id]["data"]["about_the_game"])
            if data[self.id]["data"]["is_free"] == False:
                embed = discord.Embed(title=f"{data[self.id]['data']['name']}     {data[self.id]['data']['price_overview']['final_formatted']}",
                                      description=formatted_des, colour=discord.Colour.random())
            elif data[self.id]["data"]["is_free"] == True:
                embed = discord.Embed(title=f"{data[self.id]['data']['name']}     FREE",
                                      description=formatted_des, colour=discord.Colour.random())
            embed.set_footer(text="Powered by ANC")
            embed.set_image(url=data[self.id]["data"]["header_image"])
            a = []
            for i in data[self.id]["data"]["genres"]:
                a.append(i["description"])
            formatted_genre = "❖".join(a)
            embed.add_field(name="✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢✢", value=" ", inline=False)
            embed.add_field(name=formatted_genre, value=" ", inline=False)
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            embed = discord.Embed(title="Sorry 😶‍🌫️", description=f"The data regarding {self.name} could not be found")
            await interaction.response.edit_message(embed=embed, view=self)

@client.command()
async def steam(ctx, *, name=''):
    if name == "":
        await ctx.send("Please Write '/stream game_name'")
        return
    sar = str(name).upper()
    matching_games = []
    except_terms = ['bundle', 'extension', 'non-game-term']
    matching_id = []
    with open('file.csv', "r", encoding='utf-8') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            list = row[0].strip()
            serial = row[1]
            is_game = re.match(r'^[A-Za-z0-9\s-]+$', list) and not any(term in list.lower() for term in except_terms)
            if is_game and list.startswith(sar):
                matching_games.append(list)
                matching_id.append(serial)

    if matching_games:
        await ctx.send("--Found Games--")
        for game, id in zip(matching_games, matching_id):
            view = MyButton(game, id, "us")
            embed = discord.Embed(title=game, description="Click the buttons below to get details!")
            await ctx.send(embed=embed, view=view)
        await ctx.send(matching_id)
        await ctx.send(matching_games)
        await ctx.send("-- That Is All --")
    else:
        await ctx.send("-- Not Found --")

async def load():
    for fname in os.listdir("./cogs"):
        if fname.endswith(".py") and not fname.startswith("_") and not fname[0].islower():
            await client.load_extension(f"cogs.{fname[:-3]}")

asyncio.run(load())
# _steam.steam_data() # To update the steam data base
with open("TOKEN", "r") as token:
        client.run(token.read())
