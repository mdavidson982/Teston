import discord, requests, json, aiohttp
from discord.ext import commands

#Start of SQL testing
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
                self.js = await r.json()
        
        if(self.js["media_type"] == "image"):
            apodEmbed = discord.Embed(title = "**" + self.js["title"] + "**")
            
            #apodEmbed.set_author(self.js["date"])
            if("hdurl" in self.js):
                apodEmbed.set_image(url = self.js["hdurl"])
                apodEmbed.set_footer(text="NASA Astronomy Picture of the Day", icon_url= "https://cdn.discordapp.com/attachments/849172801076199495/1049776014131200021/nasa-logo-web-rgb.png")
            else:
                apodEmbed.set_image(self.js["url"])
                apodEmbed.set_footer("NASA Astronomy Picture of the Day", icon_url= "https://cdn.discordapp.com/attachments/849172801076199495/1049776014131200021/nasa-logo-web-rgb.png")
        

        await ctx.send(embed=apodEmbed)




    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            selected_channel = guild.get_channel(785260436568276992)
            print(selected_channel)
            if(selected_channel != None):
                print("test server")
            else:
                print("ndom lmao")

#async def sendMessage():
    #guild = client.get_guild(785260019209863220)
    #channel = guild.get_channel(785260019209863223)
    #async guild.channel.send("sent on start")
async def setup(bot):
    await bot.add_cog(nasa(bot))