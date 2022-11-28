import discord, requests, json
from discord.ext import commands


class nasa(commands.Cog):
    def __inti__(self,bot):
        self.bot=bot

    @commands.command()
    async def apod(self,ctx):
        api_key ="0XlU1S3AcEWP6Is3X30bqGgBT9Hx04UcYsW6k1N1"
        base_url = "https://api.nasa.gov/planetary/apod?api_key="
        response = requests.get(base_url + api_key)
        
        file = response.json()
        await ctx.send(file)

async def setup(bot):
    await bot.add_cog(nasa(bot))