import discord, csv, re
from discord.ext import commands, tasks

from cogs.steam import steam_embed

class Steam(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
    @commands.command()
    async def steam(self, ctx, *, name = ''):
        if name == "":
            await ctx.send("Please Write '/stream game_name'")
            return 
        matching_games = []
        matching_id = []     
        sar = str(name).upper()
        except_terms = ['bundle', 'extension', 'non-game-term', 'map' , 'skins', 'dlc' , '-' , 'profiles', 'tools' , 'test' , 'teaser']
        
        print(sar)
        with open("./cogs/steam/file.csv", "r", encoding = 'utf-8') as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                list = row[0].strip()
                serial = row[1]
                is_game = re.match(r'^[A-Za-z0-9\s-]+$', list) and not any(term in list.lower() for term in except_terms)
                # Search and match the names from database 
                if is_game and  list.startswith(sar):
                    matching_games.append(list)
                    matching_id.append(serial)

        if matching_games:
                await ctx.send("--Found Games--")
                for game,id in zip(matching_games,matching_id):       
                    view = steam_embed.Button(game,id,"us")
                    embed = discord.Embed(title = game, description = "Click the button below to get the detail!")  
                    await ctx.send( embed = embed , view = view)
                
                await ctx.send("-- That Is All --")
        else: 
                await ctx.send("-- Not Found --")  
        
        print(matching_games)
        print(matching_id)
        print(len(matching_games))

async def setup(client):
    await client.add_cog(Steam(client))