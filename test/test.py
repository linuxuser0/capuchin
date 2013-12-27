import os
from capuchin import *

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CORPUS_DIR = os.path.join(CURRENT_DIRECTORY, "test_corpus")
FEED_DIR = os.path.join(CURRENT_DIRECTORY, "test_feed")

imagefeed = imagefeeds.ImageFeed(CORPUS_DIR, FEED_DIR)
imprinter = imprinters.Imprinter(imagefeed)
monkey = monkeys.StaticMonkey(imprinter)

print monkey.run()
