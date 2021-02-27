import os
from random import choice, randint

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

verb_file = open('verbs.txt')
kinks_file = open('tags_sex.txt')
otags_file = open('tags_other.txt')
chars_file = open("characters.txt")

verb_raw = verb_file.read()
kinks_raw = kinks_file.read()
otags_raw = otags_file.read()
chars_raw = chars_file.read()

verb = verb_raw.split('\n')
kinks = kinks_raw.split('\n')
other_tags = otags_raw.split('\n')
character = chars_raw.split('\n')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    userInput = message.content.lower()
    if userInput == "slash me daddy":
        kinkList = []
        for tag in range(randint(3, 5)):
            kinkList.append(choice(kinks))
        othertaglist = []
        for tag in range(randint(2, 4)):
            othertaglist.append(choice(other_tags))
        
        response = f"{choice(character)} {choice(verb)} {choice(character)}. Tags: {', '.join(kinkList)}, {', '.join(othertaglist)}"
        await message.channel.send(response)
        
client.run(TOKEN)
