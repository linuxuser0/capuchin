import os
from capuchin import *

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CORPUS_DIR = os.path.join(CURRENT_DIRECTORY, "test_corpus")
FEED_DIR = os.path.join(CURRENT_DIRECTORY, "test_feed")
SORTED_DIR = os.path.join(CURRENT_DIRECTORY, "sorted_dir")

imagefeed = imagefeeds.ImageFeed(CORPUS_DIR, FEED_DIR)
imprinter = imprinters.Imprinter(imagefeed, SORTED_DIR, 2, 1)
monkey = monkeys.StaticWindowMonkey(imprinter, 3)

print monkey.run()
