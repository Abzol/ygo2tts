#!/usr/bin/python3

from PIL import Image
import time
import requests
import sys
import os
import os.path
import json
import copy

CARD_SIZE  = (421, 614) #ygopro uploads are this size
DECK_SIZE  = (10, 4)
EXTRA_SIZE = (5, 3)

#URL_BASE = 'https://yugioh.fandom.com/wiki/'
#URL_BASE = 'https://db.ygoprodeck.com/card/?search='
URL_BASE = 'https://ygoprodeck.com/pics/'

def render_stable(path, filename):
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

def render_beta(path, filename, docpath):
    print('Paste URL for Main and Extra deck sleeves (leave blank for default backs).')
    main_back = input("Main Deck sleeves: ")
    if (main_back == ''):
        main_back = 'https://i.imgur.com/UjbK2Wb.png'
    extra_back = input("Extra Deck sleeves: ")
    if (extra_back == ''):
        extra_back = 'https://i.imgur.com/UjbK2Wb.png'
    with open('format.json', 'r') as infile:
        fmt = json.load(infile)
        data = fmt['format']
        deck_fmt = fmt['deck']
        card_fmt = fmt['card']
        contain_fmt = fmt['contain']
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
    for deck in ['main', 'extra']:#, 'side']:
        deckjson = copy.deepcopy(deck_fmt)
        if len(DECKS[deck]) > 1:
            print('---Adding', deck, 'deck---')
            if (deck == 'main'):
                cards = maindeck
                offset = 41
            elif (deck == 'extra'):
                cards = extradeck
                offset = 101
                deckjson['Transform']['posX'] = -2.5
            for index, card in enumerate(cards):
                url = URL_BASE + card + '.jpg'
                deckjson['DeckIDs'].append((offset+index)*100)
                c = dict(card_fmt)
                c['FaceURL'] = url
                if (deck == 'main'):
                    c['BackURL'] = main_back
                elif (deck == 'extra'):
                    c['BackURL'] = extra_back
                deckjson['CustomDeck'][str(offset+index)] = c
                contain = dict(contain_fmt)
                contain['CardID'] = (offset+index)*100
                deckjson['ContainedObjects'].append(contain)
                print('Added', card)
        data['ObjectStates'].append(deckjson)
    try:
        if docpath == "":
            docpath = os.path.expanduser('~/Documents/My Games/Tabletop Simulator/Saves/Saved Objects/')
            if not (os.path.isdir(os.path.join(docpath, 'ygo2tts/'))):
                os.mkdir(os.path.join(docpath, 'ygo2tts'))
            docpath = os.path.join(docpath, 'ygo2tts/')
    except Exception as e:
        print(e)
        print('You likely need to input your Tabletop Sim folder manually.')
        print('You can do this in the included ygo2tts_config.json file.')
        print('The target path should be (user)/Documents/My Games/Tabletop Simulator/Saves/Saved Objects/')
        input('Press enter to exit')
        sys.exit()
    with open(os.path.join(docpath, ''.join(filename.split('.')[:-1]) + '.json'), 'w') as of:
        json.dump(data, of, indent=2)
    r = requests.get(main_back)
    if not (os.path.isdir('./img/')):
        os.mkdir('./img')
    main_back_fn = "".join(main_back.split('/')[-1:])
    with open('./img/' + main_back_fn, 'wb') as of:
        of.write(r.content)
    im = Image.open('./img/' + main_back_fn)
    im.thumbnail((256,256), resample=Image.BICUBIC)
    im.save(os.path.join(docpath, ''.join(filename.split('.')[:-1]) + '.png'))

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Please submit a decklist')
        sys.exit()
    path, filename = os.path.split(sys.argv[1])
    with open('ygo2tts_config.json', 'r') as f:
        config = json.load(f)
    if config['beta'] == False:
        render_stable(path, filename)
    else:
        render_beta(path, filename, config['docpath'])