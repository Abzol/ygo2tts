# ygo2tts
A script to take in a .ydk file, the yu-gi-oh deck format, and push it to (a number of) .png files for use in Tabletop Simulator.

usage:
> $python3 ygo2tts.py (file)

ydk (or similar deck list) files should contain one #main heading, followed by 40 lines of card numbers. That list will be output as a png named the same as the input file, but with *-main* attached to the end. If the ydk contains either #extra or !side, it will output a similarly named file (*-extra* or *-side*). If no headings are found, it's assumed the decklist is simply a list of 40 maindeck cards.
(These numerical IDs the card database uses is printed in the lower-left corner on all cards.)

Requirements:
- python3 (to my knowledge any version), 
- [requests](https://requests.readthedocs.io/en/master/)

For windows users, there's a prebuilt binary:
- [releases](https://github.com/Abzol/ygo2tts/releases)

# Importing into Tabletop Simulator
To import into Tabletop Simulator, press *Objects*, then *Components*, and create a *Custom Deck*.
The main deck should be imported with the settings:

Width: 10, Height: 4, Number: 40

...while extra and side decks should use:

Width: 5, Height: 3, Number: 15

Remember to tick the *Back is hidden* checkbox for all decks, or face-up cards in hidden zones (including hands) will show as the last card in your decklist rather than your chosen back side.

# Custom Card images
If you'd rather use a custom card image instead of the default one provided by ygoprodecks, simply save your image of choice as a .jpg or .png in the `./img/` folder with the correct name (the id of the card visible in the lower left corner), then run the script over your deck list again. The dimensions of the file do not matter - they will be scaled to be uniform with the remainder of the deck (421 by 614 pixels).