import os
import shutil
from capuchin.imagefeeds import ImageFeed

class TestImageFeed:
    
    def setUp(self):
        self.imagefeed = ImageFeed()
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.feed_location = os.path.join(self.current_directory, "data", "feed") 
        self.imagefeed.feed_location = self.feed_location
        try:
            shutil.rmtree(self.feed_location)
        except OSError:
            pass

        os.makedirs(self.feed_location)

    def test_imagefeed_exists(self):
        assert self.imagefeed is not None

    def test_imagefeed_feeds(self):
        self.imagefeed.feed()
        assert os.listdir(self.feed_location) != []

                

