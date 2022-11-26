import discord
from discord.ext import commands
import sys, traceback, os

api_key = "2025f97dbddcd68e4dfee40ca51b25dc"
class MiniWeston(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('-'), intents=intents)


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


    async def setup_hook(self):
        for filename in os.listdir('./Mini Weston/modules'):
            if filename.endswith('.py'):
                await self.load_extension(f'modules.{filename[:-3]}')

bot = MiniWeston()
bot.run('MTA0MTQ0MjcwMTI3NjYxODg5Mg.G3JFaT.7IM--DgpPl3pj7wJRtdfCd7zEJtK-ATjPBvpSY')