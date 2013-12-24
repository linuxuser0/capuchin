from capuchin.imprinters import Imprinter
from capuchin.imagefeeds import ImageFeed

class TestImprinter:

    def setUp(self):
        self.imagefeed = ImageFeed()
        self.imprinter = Imprinter(self.imagefeed)

    def test_imprinter_exists(self):
        assert self.imprinter is not None

    def test_imprinter_imprints(self):
        test_images = self.imagefeed.feed()
        assert self.imprinter.imprint(test_images) is not None

    def test_imprinter_imagefeed_exists(self):
        assert self.imprinter.imagefeed is not None

    def test_imprinter_imagefeed_feeds_images(self):
        assert self.imprinter.imagefeed.feed() is not None

    def test_imprinter_feeds_and_imprints(self):
        assert self.imprinter.feed_and_imprint() is not  None
