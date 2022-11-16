import discord, json, requests
from discord.ext import commands


api_key = "2025f97dbddcd68e4dfee40ca51b25dc"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="-")


def getWeather(lat,lon,cityName):
        url = "https://api.openweathermap.org/data/2.5/weather?" + "appid=" + api_key + "&lat=" + str(lat) + "&lon=" + str(lon) + "&units=imperial"
        response = requests.get(url)
        file = response.json()
        data = file["main"]
        description = file["weather"]
        country = file["sys"]
        temp = data["temp"]
        

        embed=discord.Embed(title=str(round(temp,2)) + "°F" , description = str(round(((temp-32) * 0.56),2)) + "°C", color=0xfbff00)
        embed.set_author(name=cityName + ", " + str(country["country"]))
        embed.set_thumbnail(url="https://images.emojiterra.com/twitter/v13.1/512px/1f327.png")
        embed.add_field(name="Condition: ", value=str(description[0]["description"]), inline=False)
        embed.add_field(name="Min", value="F (c)", inline=True)
        embed.add_field(name="Max", value="F(c)", inline=True)
        embed.add_field(name="Humidity", value="n%", inline=True)
        embed.add_field(name="Wind", value="Speed n", inline=False)
        embed.set_footer(text="Lat: " + str(lat) + " " + "Lon: " + str(lon))
        return embed



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
        await interaction.response.edit_message(content=f"This is a new message")

@bot.command()
async def button(ctx):
    print("Running")
    await ctx.reply("This message has buttons!",view=Buttons())


@bot.command()
async def testembed(ctx, input):

    if input.isdigit():
        myEmbed = discord.Embed(title = "Just testing this shit out rq", color = 0xffffff)
        myEmbed.add_field(name = "test for the folks", inline = False, value = "putin some shit here")
        await ctx.send(embed=myEmbed)
    else:
        await ctx.send(content = "Uhh, try again chief")

@bot.command()
async def weather(ctx, *args):
    baseURL = "http://api.openweathermap.org/geo/1.0/direct?q="
    inputArgsReader = ' '.join(args)
    positionArray = inputArgsReader.split(",")
    
    if(len(positionArray) == 3):
        url = baseURL + positionArray[0] + "," + positionArray[1] + "," + positionArray[2] + "&limit=1&appid=" + api_key
        response = requests.get(url)
    elif(len(positionArray) == 2):
        url = baseURL + positionArray[0] + "," + positionArray[1] + "&limit=1&appid=" + api_key
        response = requests.get(url)
    elif(len(positionArray) == 1):
        url = baseURL + positionArray[0] + "&limit=1&appid=" + api_key 
        response = requests.get(url)
    else:
        await ctx.send(content = "Too many inputs")

    file = response.json()
    if (len(file) == 0):
        await ctx.send("Nothing found, please try to be more specific")
    else:
        place=file[0]
        await ctx.send(embed = getWeather(place["lat"],place["lon"],positionArray[0]))

bot.run('MTA0MTQ0MjcwMTI3NjYxODg5Mg.G3JFaT.7IM--DgpPl3pj7wJRtdfCd7zEJtK-ATjPBvpSY')
