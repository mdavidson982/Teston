import discord, json
from discord.ext import commands



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="-")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

class Buttons(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Button", style=discord.ButtonStyle.gray)
    async def gray_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message(content=f"This is a new message")


class TestButtons(discord.ui.View):
    def __inti__(self,*,timeout=180):
        super().__inti__(timeout=timeout)
    @discord.ui.button(label="New Button!", style=discord.ButtonStyle.gray)
    async def gray_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        button.style = discord.ButtonStyle.red
        button.disabled = True
        await interaction.response.edit_message(content = "Borked" , view=self)
        await interaction.followup.send(content = "Button pressed.", ephemeral = True)

@bot.command()
async def button(ctx):
    print("Running")
    await ctx.reply("This message has buttons!",view=TestButtons())


bot.run('MTA0MTQ0MjcwMTI3NjYxODg5Mg.G3JFaT.7IM--DgpPl3pj7wJRtdfCd7zEJtK-ATjPBvpSY')
