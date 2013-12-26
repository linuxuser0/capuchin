import os
import shutil
from capuchin.imagefeeds import ImageFeed
from config import *

class TestImageFeed:
    
    def setUp(self):
        self.imagefeed = ImageFeed(feed_location=TEST_FEED_LOCATION)
        self.current_directory = os.path.dirname(os.path.realpath(__file__))

    def test_imagefeed_exists(self):
        assert self.imagefeed is not None

    def test_imagefeed_feeds(self):
        self.imagefeed.feed()
        assert os.listdir(TEST_FEED_LOCATION) != []

                

