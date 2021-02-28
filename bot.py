import os, json
from random import choice, randint

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

class File_Stuff:
    verb_file = open('verbs.json').read()
    kinks_file = open('tags_sex.json').read()
    otags_file = open('tags_other.json').read()
    chars_file = open("characters.json").read()
    ChSpVe_file = open("char_spec_verbs.json").read() # "Character Specific Verbs", as in verbs that only apply to one character
    verb = json.loads(verb_file)
    kinks = json.loads(kinks_file)
    other_tags = json.loads(otags_file)
    character = json.loads(chars_file)
    ChSpVe = json.loads(ChSpVe_file)

@bot.command(name="slashmedaddy")
async def randomSlash(ctx):
    kinkList = []
    for tag in range(randint(3, 5)):
        kinkList.append(choice(File_Stuff.kinks))
    othertagList = []
    for tag in range(randint(2, 4)):
        othertagList.append(choice(File_Stuff.other_tags))
    
    firstChar = choice(File_Stuff.character)
    if File_Stuff.ChSpVe[firstChar] != [""]:
        File_Stuff.verb.append(File_Stuff.ChSpVe[firstChar])
    secondChar = choice(File_Stuff.character)
    
    response = f"{firstChar} {choice(File_Stuff.verb)} {secondChar}. Tags: {', '.join(kinkList)}, {', '.join(othertagList)}"
    await ctx.send(response)
    if File_Stuff.ChSpVe[firstChar] in File_Stuff.verb:
        File_Stuff.verb.remove(File_Stuff.ChSpVe[firstChar])
        
bot.run(TOKEN)
