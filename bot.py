import os, json
from random import choice, randint

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")
godKing = "Kulemi#4082"

class File_Stuff:
    verb_file = open('verbs.json')
    verb_raw = verb_file.read()
    kinks_file = open('tags_sex.json')
    kinks_raw = kinks_file.read()
    otags_file = open('tags_other.json')
    otags_raw = otags_file.read()
    ChSpVe_file = open("char_spec_verbs.json") # "Character Specific Verbs", as in verbs that only apply to one character
    ChSpVe_raw = ChSpVe_file.read()
    verb = json.loads(verb_raw)
    kinks = json.loads(kinks_raw)
    other_tags = json.loads(otags_raw)
    character = list(json.loads(ChSpVe_raw).keys())
    ChSpVe = json.loads(ChSpVe_raw)
    
async def slashGen(firstChar, ctx):
    kinkList = []
    for tag in range(randint(3, 5)):
        kinkList.append(choice(File_Stuff.kinks))
    othertagList = []
    for tag in range(randint(2, 4)):
        othertagList.append(choice(File_Stuff.other_tags))
    
    ChSpVeFirst = File_Stuff.ChSpVe[firstChar]
    if ChSpVeFirst != [""]:
        for ChSpVeIndv in ChSpVeFirst: # ChSpVeIndv = Character Specific Verb, Individual. These are fucking awful variable names
            File_Stuff.verb.append(ChSpVeIndv)
    secondChar = choice(File_Stuff.character)
    
    response = f"{firstChar} {choice(File_Stuff.verb)} {secondChar}. Tags: {', '.join(kinkList)}, {', '.join(othertagList)}"
    await ctx.send(response)
    
    for ChSpVeIndv in ChSpVeFirst:
        if ChSpVeIndv in File_Stuff.verb:
            File_Stuff.verb.remove(ChSpVeIndv)
    
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.command(name="slashmedaddy")
async def randomSlash(ctx):
    firstChar = choice(File_Stuff.character)
    await slashGen(firstChar, ctx)

@bot.command(name="slash")
async def specSlash(ctx, *userInput):
    inputChar = " ".join(userInput)
    if inputChar in File_Stuff.character:
        firstChar = inputChar
        await slashGen(firstChar, ctx)
    else:
        await ctx.send(f"Cannot find character {inputChar}")
        
@bot.command(name="password")
async def password(ctx, passwordInput):
    if passwordInput == "Copacetic":
        global godKing
        godKing = ctx.message.author
        await ctx.send("Of course, master.")
    else:
        await ctx.send("You are a false king!")
        
@bot.command(name="update")
async def updateFiles(ctx):
    if ctx.message.author == godKing:
        File_Stuff.verb_file.close()
        File_Stuff.verb_file = open('verbs.json').read()
        
        File_Stuff.kinks_file.close()
        File_Stuff.kinks_file = open('tags_sex.json').read()
        
        File_Stuff.otags_file.close()
        File_Stuff.otags_file = open('tags_other.json').read()
        
        File_Stuff.ChSpVe_file.close()
        File_Stuff.ChSpVe_file = open("char_spec_verbs.json").read()
        await ctx.send("Updated files.")
    else:
        await ctx.send(f"You are not the admin. The admin is {godKing}, and you are {ctx.message.author}")
bot.run(TOKEN)
