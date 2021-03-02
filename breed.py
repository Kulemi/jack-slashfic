import json, random

snip_file = open('snips.json')
snip_raw = snip_file.read()
snip_list = json.loads(snip_raw)
snip_file.close()


def spawner(firstChar, secondChar):
    randomSnip = random.choice(snip_list)
    return randomSnip.format(firstChar, secondChar)

def update():
    snip_file = open('snips.json')
    snip_raw = snip_file.read()
    snip_list = json.loads(snip_raw)
    snip_file.close()