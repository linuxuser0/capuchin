from capuchin.imprinters import Imprinter
from capuchin.imagefeeds import ImageFeed
from config import *

class TestImprinter:

    def setUp(self):
        self.imagefeed = ImageFeed(feed_location = TEST_FEED_LOCATION)
        self.imprinter = Imprinter(feed_location = TEST_FEED_LOCATION)

    def test_imprinter_exists(self):
        assert self.imprinter is not None

    def test_imprinter_imprints(self):
        self.imagefeed.feed()
        assert self.imprinter.imprint() is not None

    def test_imprinter_imagefeed_exists(self):
        assert self.imprinter.imagefeed is not None

    def test_imprinter_imagefeed_feeds_images(self):
        assert self.imprinter.imagefeed.feed() is not None

    def test_imprinter_feeds_and_imprints(self):
        assert self.imprinter.feed_and_imprint() is not  None
