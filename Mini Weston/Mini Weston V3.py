
#REALLY IMPORTANT.
#PRIVATE IS A LOCAL FILE THAT STORES THE API CODE. IT IS NOT ON GITHUB.
import Private as p
import discord
from discord.ext import commands
import sys, traceback, os

class MiniWeston(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('-'), intents=intents)


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


    async def setup_hook(self):
        for filename in os.listdir('./modules'):
            if filename.endswith('.py'):
                await self.load_extension(f'modules.{filename[:-3]}')

bot = MiniWeston()
bot.run(p.DISCORD_API_KEY)