import discord
from discord.ext import commands

class test(commands.Cog):
    def __inti__(self,bot):
        self.bot=bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Yep, this test worked.")

async def setup(bot):
    await bot.add_cog(test(bot))
