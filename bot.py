import os, json, breed
from random import choice, randint

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")
godKing = 79667388269731840

class File_Stuff:
    verb_file = open('verbs.json')
    verb_raw = verb_file.read()
    kinks_file = open('tags_sex.json')
    kinks_raw = kinks_file.read()
    tags_file = open('tags_other.json')
    tags_raw = tags_file.read()
    ChSpVe_file = open("char_spec_verbs.json") # "Character Specific Verbs", as in verbs that only apply to one character
    ChSpVe_raw = ChSpVe_file.read()
    verb = json.loads(verb_raw)
    kinks = json.loads(kinks_raw)
    tags = json.loads(tags_raw)
    character = list(json.loads(ChSpVe_raw).keys())
    ChSpVe = json.loads(ChSpVe_raw)
    
    
class Discord_Stuff:
    kink_s_channel = 815007678472519680
    tag_s_channel = 815208435960119347
    verb_s_channel = 815217396109410325
    char_s_channel = 815704435988234280

File_Start = File_Stuff()
File_Ongoing = File_Start
async def slashGen(firstChar, ctx):
    kinkList = []
    for tag in range(randint(3, 5)):
        kinkList.append(choice(File_Ongoing.kinks))
    tagsList = []
    for tag in range(randint(2, 4)):
        tagsList.append(choice(File_Ongoing.tags))
    
    ChSpVeFirst = File_Ongoing.ChSpVe[firstChar]
    if ChSpVeFirst != [""]:
        for ChSpVeIndv in ChSpVeFirst: # ChSpVeIndv = Character Specific Verb, Individual. These are fucking awful variable names
            File_Ongoing.verb.append(ChSpVeIndv)
    secondChar = choice(File_Ongoing.character)
    
    response = f"{firstChar} {choice(File_Ongoing.verb)} {secondChar}. Tags: {', '.join(kinkList)}, {', '.join(tagsList)}"
    await ctx.send(response)
    
    for ChSpVeIndv in ChSpVeFirst:
        if ChSpVeIndv in File_Ongoing.verb:
            File_Ongoing.verb.remove(ChSpVeIndv)
    
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.command(name="slashmedaddy", brief="Randomly match 2 characters")
async def randomSlash(ctx):
    firstChar = choice(File_Ongoing.character)
    await slashGen(firstChar, ctx)

@bot.command(name="slash", brief="Choose one character to slash with another (random) character")
async def specSlash(ctx, *userInput):
    firstChar = " ".join(userInput)
    await slashGen(firstChar, ctx)
        
@bot.command(name="fanfic", brief="Create a small cursed snippet involving 1 or more characters.")
async def fanfic(ctx, *userInput):
    firstChar = " ".join(userInput)
    secondChar = choice(File_Stuff.character)
    if firstChar == "random":
        await ctx.send(breed.spawner(choice(File_Stuff.character), secondChar))
    elif firstChar == "":
        await ctx.send("Please include a character, or use \"random\" to randomly choose a character.")
    else:
        await ctx.send(breed.spawner(firstChar, secondChar))
        
        
@bot.command(name="password", brief="Not yet implemented lmfao")
async def password(ctx, passwordInput):
    if passwordInput == "Copacetic":
        global godKing
        godKing = ctx.message.author.id
        await ctx.send("You are the new admin. Use this power wisely.")
    else:
        await ctx.send("Incorrect password.")
        
@bot.command(name="update", brief="Admin thing for updating files.")
async def updateFiles(ctx):
    if ctx.message.author.id == godKing:
        File_Ongoing = File_Stuff()
        breed.update()
        await ctx.send("Updated files.")
    else:
        await ctx.send(f"You are not the admin. The admin is {godKing}, and you are {ctx.message.author.id}")
        
@bot.command(name="suggest", brief="Suggest a character, kink, tag, or verb")
async def suggest(ctx, stype_raw, *suggestion_raw):
    stype = stype_raw.lower()
    suggestion = " ".join(suggestion_raw)
    stypesDict = {"character":File_Ongoing.character, "kink":File_Ongoing.kinks, "tag":File_Ongoing.tags, "verb":File_Ongoing.verb}
    if stype in stypesDict.keys():
        if suggestion in stypesDict[stype]:
            await ctx.send("Your suggestion is already in the list.")
        else:
            channelDict = {"character":Discord_Stuff.char_s_channel,"kink":Discord_Stuff.kink_s_channel,"tag":Discord_Stuff.tag_s_channel,"verb":Discord_Stuff.verb_s_channel}
            channel = bot.get_channel(channelDict[stype])
            await channel.send(suggestion)
            await ctx.send("Your suggestion is being considered.")
    else:
        await ctx.send(f"{stype_raw} is not a valid suggestion type. The allowed suggestion types are (without quotes): \"character\", \"kink\", \"tag\", and \"verb\".")
    #check the rest against the appropriate lists
    
    
bot.run(TOKEN)
