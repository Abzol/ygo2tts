#!/usr/bin/python3

from PIL import Image
import time
import requests
from bs4 import BeautifulSoup
import sys
import os.path

CARD_SIZE  = (500, 710)
DECK_SIZE  = (10, 4)
EXTRA_SIZE = (5, 3)

URL_BASE = 'https://yugioh.fandom.com/wiki/'
#URL_BASE = 'https://db.ygoprodeck.com/card/?search='

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Please submit a decklist')
        sys.exit()
    deckname = sys.argv[1]
    with open(sys.argv[1], 'r') as f:
        state = 'MAIN'
        maindeck  = []
        extradeck = []
        sidedeck  = []
        for line in f.readlines():
            try:
                if (len(line)<2): #blank line
                    continue
                text = line.lstrip()[3:]
                if (text.startswith('MONSTER') or text.startswith('SPELL') or text.startswith('TRAP')):
                    continue #no reason to tag here
                elif (text.startswith('EXTRA DECK')):
                    state = 'EXTRA'
                elif (text.startswith('SIDE DECK')):
                    state = 'SIDE'
                elif (text[0].isnumeric()):
                    number, name = text.split(maxsplit=1)
                    if (state == 'MAIN'):
                        maindeck.append((number[:-1], name.rstrip()))
                    elif (state == 'EXTRA'):
                        extradeck.append((number[:-1], name.rstrip()))
                    elif (state == 'SIDE'):
                        sidedeck.append((number[:-1], name.rstrip()))
                else:
                    print('Malformed input!')
                    print(line)
                    continue
            except:
                print('Malformed input! -EXCEPTION-')
                print(line)
                continue
    #main deck
    for deck in ['main', 'extra']:
        position = (0, 0)
        if (deck == 'main'):
            deckimage = Image.new('RGB', tuple(l * r for l, r in zip(CARD_SIZE, DECK_SIZE)))
            cards = maindeck
            DECKTYPE_SIZE = DECK_SIZE
        elif (deck == 'extra'):
            deckimage = Image.new('RGB', tuple(l * r for l, r in zip(CARD_SIZE, EXTRA_SIZE)))
            cards = extradeck
            DECKTYPE_SIZE = EXTRA_SIZE
        for card in cards:
            r = requests.get(URL_BASE + card[1])
            soup = BeautifulSoup(r.text, 'html.parser')
            cardimage = soup.find('td', class_='cardtable-cardimage').next_element.next_element['src']
            cardimage = cardimage[0:cardimage.find('.png')+4]
            ci = requests.get(cardimage)
            with open('tmp.png', 'wb') as of:
                of.write(ci.content)
            im = Image.open('tmp.png')
            im = im.resize(CARD_SIZE, resample=Image.BICUBIC)
            for _ in range(int(card[0])):
                deckimage.paste(im, (CARD_SIZE[0] * position[0], CARD_SIZE[1] * position[1]))
                if (position[0] < (DECKTYPE_SIZE[0] - 1)):
                    position = (position[0]+1, position[1])
                elif (position[0] == (DECKTYPE_SIZE[0] -1)):
                    position = (0, position[1]+1)
            print('Added', card[1])
            time.sleep(1.0)
        deckimage.save(deckname + '-' + deck + '.png')