import discord, requests, json, aiohttp
from discord.ext import commands


class nasa(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.API_KEY = "0XlU1S3AcEWP6Is3X30bqGgBT9Hx04UcYsW6k1N1"
        #print("Yeah, nada loaded")

    @commands.command()
    async def apod(self,ctx):
        base_url = "https://api.nasa.gov/planetary/apod?api_key="
        
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url + self.API_KEY) as r:
                js = await r.json()
                print(self.API_KEY)
        await ctx.send(js)


    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            selected_channel = guild.get_channel(785260436568276992)
            print(selected_channel)
            if(selected_channel != None):
                await selected_channel.send("Worked?")
            else:
                print("ndom lmao")

#async def sendMessage():
    #guild = client.get_guild(785260019209863220)
    #channel = guild.get_channel(785260019209863223)
    #async guild.channel.send("sent on start")
async def setup(bot):
    await bot.add_cog(nasa(bot))