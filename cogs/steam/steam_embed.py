import discord, json, requests, re
from discord.ui import Button
from discord.ext import commands

class Button(discord.ui.View):
    def __init__(self, name, id, region):
        super().__init__()
        self.name = name
        self.id = id
        self.region = region
        # self.add_item(Button(label = "US", custom_id="my_button0"))
        # self.add_item(Button(label = "ARS", custom_id="my_button1")

    @discord.ui.button(label="GetDetail(US)", style=discord.ButtonStyle.green, custom_id="button_us")
    async def us_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_game_details(interaction, self.region)

    @discord.ui.button(label="GetDetail(ARS)", style=discord.ButtonStyle.green, custom_id="button_ars")
    async def ars_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_game_details(interaction, "ar")
    
    @discord.ui.button(label="GetDetail(TL)", style=discord.ButtonStyle.green, custom_id="button_tl")
    async def tl_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_game_details(interaction, "tr")

    @discord.ui.button(label="GetDetail(INDIA)", style=discord.ButtonStyle.green, custom_id="button_₹")
    async def in_button_callback(self,interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_game_details(interaction,'in')

    async def send_game_details(self, interaction, region):
        url = f"https://store.steampowered.com/api/appdetails/?appids={self.id}&cc={region}&l=en"
        response = requests.get(url)
        data = json.loads(response.text)
        
        if data[self.id]["success"] == True:
            if not "price_overview" in data[self.id]['data']:
                embed = discord.Embed(title="Sorry 😶‍🌫️", description=f"The data regarding {self.name} could not be found")
                await interaction.response.edit_message(embed=embed , view=self)
            else:
                formatted_des = re.sub("<.*?>", "", data[self.id]["data"]["about_the_game"])
            if data[self.id]["data"]["is_free"] == False:
                formatted_des = re.sub("<.*?>", "", data[self.id]["data"]["about_the_game"])
                embed = discord.Embed(title=f"{data[self.id]['data']['name']}     {data[self.id]['data']['price_overview']['final_formatted']}",
                                      description=formatted_des, colour=discord.Colour.random())
            elif data[self.id]["data"]["is_free"] == True:
                formatted_des = re.sub("<.*?>", "", data[self.id]["data"]["about_the_game"])
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





