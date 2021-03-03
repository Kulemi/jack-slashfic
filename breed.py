import json, random

snip_file = open('snips.json')
snip_raw = snip_file.read()
snip_list = json.loads(snip_raw)
snip_file.close()


def spawner(firstChar, secondChar, thirdChar, fourthChar, fifthChar):
    randomSnip = random.choice(snip_list)
    return randomSnip.format(firstChar, secondChar, thirdChar, fourthChar, fifthChar)

def update_local():
    snip_file = open('snips.json')
    snip_raw = snip_file.read()
    global snip_list
    snip_list = json.loads(snip_raw)
    snip_file.close()

def update():
    edit_snip_file = open('snips.json', 'w')
    json.dump(snip_list, edit_snip_file, indent=2)
    edit_snip_file.close()