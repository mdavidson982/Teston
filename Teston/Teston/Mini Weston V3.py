import os
from discord.ext import commands

class Teston(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
    for folder in os.listdir("modules"):
        if os.path.exisst(os.path.join("modules", folder, "cog.py")):
            client.load_extension(f"modules.{folder}.cog")


    def coinflip(self):
        return random.randint(0, 1)

    @commands.command()
    async def test(self, ctx):
        """Gambles some money."""
        test = test(bot)
        test.testCommand(ctx.author)

        