import discord
from discord.ext import commands


class nasa(commands.Cog):
    def __inti__(self,bot):
        self.bot=bot

async def setup(bot):
    await bot.add_cog(nasa(bot))