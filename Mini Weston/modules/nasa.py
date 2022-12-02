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
        embed=discord.Embed(title="TEST")
        embed.set_image(url= "https://apod.nasa.gov/apod/image/2201/RhoOphAntares_Cogo_1024.jpg")
        #embed.set_footer(text= "url: https://www.youtube.com/embed/s6IpsM_HNcU?rel=0")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(nasa(bot))