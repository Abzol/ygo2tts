# ygo2tts
A script to take in a .ydk file, the yu-gi-oh deck format, and push it to (a number of) .png files for use in Tabletop Simulator.

usage:
> $python3 ygo2tts.py (file)

ydk files should contain one #main heading, followed by 40 lines of card numbers. That list will be output as a png named the same as the ydk input file, but with *-main* attached to the end. If the ydk contains either #extra or !side, it will output a similarly named file (*-extra* or *-side*)

To import into Tabletop Simulator, the main deck should be imported with the settings:

*Width*: 10, *Height*: 4, *Number*: 40, *Back is Hidden*: True

...while extra decks and side decks should use:

*Width*: 5, *Height*: 3, *Number*: 15, *Back is Hidden*: True