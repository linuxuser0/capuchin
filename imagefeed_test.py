from capuchin import *
from config import *
import os
im = imagefeeds.ImageFeed(IMAGE_LOCATION, FEED_LOCATION)
im.feed(5)
im.feed(5)
im.feed(5)
print len(os.listdir(FEED_LOCATION))
