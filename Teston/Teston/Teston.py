import discord, json, requests, emoji, unicodedata
from discord.ext import commands
from discord.ui import Select, View


api_key = "2025f97dbddcd68e4dfee40ca51b25dc"
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('-'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


bot = Bot()


def flag_for(code):
    """Return unicode flag emoji given a 2-digit country code."""
    return "".join(
        unicodedata.lookup(f"REGIONAL INDICATOR SYMBOL LETTER {char}")
        for char in code
    )

def embedMaker():
    embed = discord.Embed(title = "Test")
    return embed
class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select a location...', min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
    # Use the interaction object to send a response message containing
    # the user's favourite colour or choice. The self object refers to the
    # Select object, and the values attribute gets a list of the user's
    # selected options. We only want the first one.
        baseURL = "http://api.openweathermap.org/geo/1.0/direct?q="
        positionArray = self.values[0].split(",")
        #If the positionArray is = 3, then it is in the US (since only US locations use the state codes)
        if(len(positionArray) == 3):
            url = baseURL + positionArray[0] + "," + positionArray[1] + "," + positionArray[2] + "&limit=10&appid=" + api_key
            response = requests.get(url)
            print("Geo URL: "+ url)

        #If the positionArray is = 2, it could be anywhere, The second input could be a state or a country code.
        elif(len(positionArray) == 2):
            url = baseURL + positionArray[0] + "," + positionArray[1] + "&limit=10&appid=" + api_key
            response = requests.get(url)
            print("Geo URL: "+ url)

        #If the positionArray is 1, then the user just entered a City name. This could be dangerous? The output might not be the city they were looking for
        elif(len(positionArray) == 1):

            url = baseURL + positionArray[0] + "&limit=10&appid=" + api_key
            response = requests.get(url)
            print("Geo URL: "+ url)
            
        file = response.json()
        place = file[0]
        await interaction.response.send_message(embed = getWeather(place["lat"],place["lon"],place["name"]))


        

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.dropdown = Dropdown()
        self.add_item(self.dropdown)



def getWeather(lat,lon,cityName):
        
        url = "https://api.openweathermap.org/data/2.5/weather?" + "appid=" + api_key + "&lat=" + str(lat) + "&lon=" + str(lon) + "&units=imperial"
        print("Weather URL: "+url)
        response = requests.get(url)
        file = response.json()
        data = file["main"]
        description = file["weather"]
        country = file["sys"]
        weather = file["wind"]
        temp = data["temp"]
        tempmin = data["temp_min"]
        tempmax = data["temp_max"]
        humidity = data["humidity"]
        symbolCode = description[0]["id"]

        if symbolCode in range(200, 805, 1):
            if symbolCode in range(200,233,1):
                #lightning
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823546117824523/cloud-with-lightning.png"
            if symbolCode in range(300,322,1):
                #rain cloud, drizzling
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545169911940/cloud-with-rain.png"
            if symbolCode in range(500,532,1):

                if(symbolCode == 511):
                    #snowflake, freezing rain
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823546432393297/snowflake.png"
                else:
                    #rain cloud
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545169911940/cloud-with-rain.png"
            if symbolCode in range(600,623,1):
                #snowflake
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823546432393297/snowflake.png"

            if symbolCode in range(701,782,1):
                #fog
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823544813404160/fog.png"
            if symbolCode == 800:
                #sunny
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545778094111/sun.png"
            if symbolCode in range(801,805,1):
                if symbolCode == 801:
                    #partly cloudy, more sun
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545480286218/sun-behind-cloud.png"
                if symbolCode == 802:
                    #partly cloudy, less sun
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1043291154214559764/partly-cloudy.png"
                if symbolCode == 803 or symbolCode == 804:
                    #clouds
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823546763755651/cloudy.png"
        else: 
            #if Code is not in range, set the URL to sunny
            Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545778094111/sun.png"

        
        embed=discord.Embed(title=str(round(temp,2)) + "°F" , description = str(round(((temp-32) * 0.56),2)) + "°C", color=0xfbff00)
        embed.set_author(name=str(cityName) + ", " + str(country["country"]))
        embed.set_thumbnail(url=Wurl)
        embed.add_field(name="Condition: ", value=str(description[0]["description"]), inline=False)
        embed.add_field(name="Min " + str(tempmin) + "°F", value = "(" + str(round(((tempmin - 32) * .56),2)) + "°C)", inline=True)
        embed.add_field(name="Max " + str(tempmax) + "°F", value = "(" + str(round(((tempmax - 32) * .56),2)) + "°C)", inline=True)
        embed.add_field(name="Humidity", value= str(humidity)+"%", inline=False)
        embed.add_field(name="Wind", value=str(weather["speed"]) + " MPH" , inline=True)
        embed.set_footer(text="Lat: " + str(lat) + " " + "Lon: " + str(lon))
        return embed



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



#Gets the weather based off a users input
#Input format: -weather City name, State code (if in US), Country code
#Country code refers to the ISO 1833 country code list.
@bot.command()
async def weather(ctx, *args):
    #The first steps of this command take the user input and converts the given city to it's coresponding Lattitude and Logittude based using the OpenWeather API
    
    #BaseURL for getting Lat and Lon
    baseURL = "http://api.openweathermap.org/geo/1.0/direct?q=" 

    #technically the command can take an infinite number of arguments, this is because some cities can be made up of more then one name
    #Ex: West Warwick
    #If this we didn't do it this way, citynames containing more then one word would have to be contained using " "
    #Which isn't user friendly


    #Using the arguments, we reduce any extra spaces by combining each argument with a single space
    #Ex: West                     Warwick,              RI, US
    #Becomes: West Warwick, RI, US
    inputArgsReader = ' '.join(args)

    #Next, we create an array by splitting each input by using ,
    positionArray = inputArgsReader.split(",")
    

    #If the positionArray is = 3, then it is in the US (since only US locations use the state codes)
    if(len(positionArray) == 3):
        url = baseURL + positionArray[0] + "," + positionArray[1] + "," + positionArray[2] + "&limit=10&appid=" + api_key
        response = requests.get(url)
        print(url)

    #If the positionArray is = 2, it could be anywhere, The second input could be a state or a country code.
    elif(len(positionArray) == 2):
        url = baseURL + positionArray[0] + "," + positionArray[1] + "&limit=10&appid=" + api_key
        response = requests.get(url)

    #If the positionArray is 1, then the user just entered a City name. This could be dangerous? The output might not be the city they were looking for
    elif(len(positionArray) == 1):

        url = baseURL + positionArray[0] + "&limit=10&appid=" + api_key
        response = requests.get(url)
        print("Geo URL: "+url)
        
    
    #If something goes wrong here, The user input was incorrect. Throw an Excetion
    
    file = response.json()

    #if no results, say that nothing was found
    print("Response Length: "+ str(len(file)))
    try:
        if (len(file) == 0):
            await ctx.send("Dumbass")
        #If one result, send the information to the getWeather function
        elif len(file) == 1:
                place = file[0]
            
                await ctx.send(embed = getWeather(place["lat"],place["lon"],place["name"]))
        #if more then one result, create a selection view where the user will be asked
        #to select on of the results. After an option is selected, display the weather for that city.
        else:
            view = DropdownView()
            newState = []
            newCountry = []
            dupState = []
            dupCountry = []
            for i in range(len(file)):
                place = file[i]
                if "state" in place:
                    if place["state"] not in newState:
                        newState.append(place["state"])


                        if(emoji.is_emoji(flag_for(place["country"]))):
                            view.dropdown.add_option(label = place["name"] + ", " + place["state"] + ", " + place["country"], emoji = flag_for(place["country"]))
                        else:
                            view.dropdown.add_option(label = place["name"] + ", " + place["state"] + ", " + place["country"])
                    else:
                        dupState.append(i)
                
                else:
                    if i not in newCountry:
                        newCountry.append(i)
                        #print(str(i) + ", ")
                        #print(place["name"] + ", " + place["country"])
                        if(emoji.is_emoji(flag_for(place["country"]))):
                            view.dropdown.add_option(label = place["name"] + ", " + place["country"], emoji = flag_for(place["country"]))
                        else:
                            view.dropdown.add_option(label = place["name"] + ", " + place["country"])
                    else:
                        dupCountry.append(i)

            await ctx.send("**multiple results found:**", view = view)

    except:
         await ctx.send("Something went wrong. Did you put the command in correctly?") 

bot.run('MTA0MTQ0MjcwMTI3NjYxODg5Mg.G3JFaT.7IM--DgpPl3pj7wJRtdfCd7zEJtK-ATjPBvpSY')