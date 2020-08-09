#!/usr/bin/python3

from PIL import Image
import time
import requests
import sys
import os

CARD_SIZE  = (421, 614) #ygopro uploads are this size
DECK_SIZE  = (10, 4)
EXTRA_SIZE = (5, 3)

#URL_BASE = 'https://yugioh.fandom.com/wiki/'
#URL_BASE = 'https://db.ygoprodeck.com/card/?search='
URL_BASE = 'https://ygoprodeck.com/pics/'

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Please submit a decklist')
        sys.exit()
    path, filename = os.path.split(sys.argv[1])
    with open(os.path.join(path, filename), 'r') as f:
        state = 'main' #assume
        maindeck  = []
        extradeck = []
        sidedeck  = []
        DECKS = {
            'main' : maindeck,
            'extra' : extradeck,
            'side' : sidedeck
        }
        for line in f.readlines():
            try:
                if (len(line)<2): #blank line
                    continue
                if (line.startswith('#main')):
                    state = 'main'
                elif (line.startswith('#extra')):
                    state = 'extra'
                elif (line.startswith('!side')):
                    state = 'side'
                elif (line.rstrip().isnumeric()):
                    DECKS[state].append(line.rstrip())
                else:
                    print('Malformed input!')
                    print(line)
                    continue
            except:
                print('Malformed input! -EXCEPTION-')
                print(line)
                continue
    #main deck
    for deck in ['main', 'extra', 'side']:
        if len(DECKS[deck]) > 1:
            print('---Adding', deck, 'deck---')
            position = (0, 0)
            if (deck == 'main'):
                deckimage = Image.new('RGB', tuple(l * r for l, r in zip(CARD_SIZE, DECK_SIZE)))
                cards = maindeck
                DECKTYPE_SIZE = DECK_SIZE
            elif (deck == 'extra' or deck == 'side'):
                deckimage = Image.new('RGB', tuple(l * r for l, r in zip(CARD_SIZE, EXTRA_SIZE)))
                if (deck == 'extra'):
                    cards = extradeck
                if (deck == 'side'):
                    cards = sidedeck
                DECKTYPE_SIZE = EXTRA_SIZE
            for card in cards:
                if not (os.path.isdir('./img/')):
                    os.mkdir('./img')
                if not (os.path.isfile('./img/' + card + '.jpg') or os.path.isfile('.img/' + card + '.png')):
                    r = requests.get(URL_BASE + card + '.jpg')
                    with open('./img/' + card + '.jpg', 'wb') as of:
                        of.write(r.content)
                    time.sleep(1.0) #be nice to the server
                im = Image.open('./img/' + card + '.jpg')
                im = im.resize(CARD_SIZE, resample=Image.BICUBIC)
                deckimage.paste(im, (CARD_SIZE[0] * position[0], CARD_SIZE[1] * position[1]))
                if (position[0] < (DECKTYPE_SIZE[0] - 1)):
                    position = (position[0]+1, position[1])
                elif (position[0] == (DECKTYPE_SIZE[0] -1)):
                    position = (0, position[1]+1)
                print('Added', card)
            deckimage.save(os.path.join(path, ''.join(filename.split('.')[:-1]) + '-' + deck + '.png'))