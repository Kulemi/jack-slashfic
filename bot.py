import os, json, breed, discord
from random import choice, randint

from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")
client = discord.Client
royalty = [79667388269731840]

class File_Stuff:
    characters_file = open("characters.json")
    characters_raw = characters_file.read()
    characters = json.loads(characters_raw)
    

class Discord_Stuff:
    snips_s_channel = 815217396109410325
    char_s_channel = 815704435988234280

File_Start = File_Stuff()
File_Ongoing = File_Start
    
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
        
@bot.command(name="fanfic", brief="Create a small cursed snippet involving 1 or more characters.")
async def fanfic(ctx, *userInput):
    firstChar = " ".join(userInput)
    secondChar = choice(File_Stuff.characters)
    thirdChar = choice(File_Stuff.characters)
    fourthChar = choice(File_Stuff.characters)
    fifthChar = choice(File_Stuff.characters)
    if firstChar == "random":
        await ctx.send(breed.spawner(choice(File_Stuff.characters), secondChar, thirdChar, fourthChar, fifthChar))
    elif firstChar == "":
        await ctx.send("Please include a character, or use \"random\" to randomly choose a character.")
    else:
        await ctx.send(breed.spawner(firstChar, secondChar, thirdChar, fourthChar, fifthChar))
        
        
@bot.command(name="password", brief="Not yet implemented lmfao")
async def password(ctx, passwordInput):
    if passwordInput == "Copacetic":
        global royalty
        royalty.append(ctx.message.author.id)
        await ctx.send("You are a new admin. Use this power wisely.")
        print(f"New admin: {ctx.message.author}")
    else:
        await ctx.send("Incorrect password.")
        
@bot.command(name="update-local", brief="Admin thing for updating files on the local computer. DO NOT USE UNLESS YOU KNOW EXACTLY WHAT YOU'RE DOING")
async def updateFiles(ctx):
    if ctx.message.author.id in royalty:
        File_Ongoing = File_Stuff()
        breed.update_local()
        await ctx.send("Updated files.")
    else:
        await ctx.send(f"You are not an admin.")
        
@bot.command(name="update", brief="Admin thing to add new, approved suggestions to the list.")
async def update(ctx):
    if ctx.message.author.id in royalty:
        edit_char_file = open("characters.json", 'w')
        json.dump(File_Ongoing.characters, edit_char_file, indent=2)
        edit_char_file.close()
        breed.update()
        await ctx.send("Updated files with new suggestions.")
        
@bot.command(name="suggest", brief="Suggest a character or snip")
async def suggest(ctx, stype_raw, *suggestion_raw):
    stype = stype_raw.lower()
    suggestion = " ".join(suggestion_raw)
    stypesDict = {"character":File_Ongoing.characters, "snip":breed.snip_list}
    if stype in stypesDict.keys():
        if suggestion in stypesDict[stype]:
            await ctx.send("Your suggestion is already in the list.")
        else:
            channelDict = {"character":Discord_Stuff.char_s_channel,"snip":Discord_Stuff.snips_s_channel}
            channel = bot.get_channel(channelDict[stype])
            await channel.send(suggestion)
            await ctx.send("Your suggestion is being considered.")
    else:
        await ctx.send(f"{stype_raw} is not a valid suggestion type. The allowed suggestion types are (without quotes): \"character\" and \"snip\". (More to come)")
    
@bot.command(name="add", brief="Admin thing to add approved suggestions manually.")
async def add_suggestion(ctx, stype_raw, *suggestion_raw):
    stype = stype_raw.lower()
    suggestion = " ".join(suggestion_raw)
    stypesDict = {"character":File_Ongoing.characters, "snip":breed.snip_list}
    if stype in stypesDict.keys():
        if suggestion in stypesDict[stype]:
            await ctx.send("Your suggestion is already in the list.")
        else:
            stypesDict[stype].append(suggestion)
            await ctx.send(f"Added \"{suggestion}\" to {stype} list")
    else:
        await ctx.send(f"{stype_raw} is not a valid suggestion type. The allowed suggestion types are (without quotes): \"character\" and \"snip\". (More to come)")
    
bot.run(TOKEN)
