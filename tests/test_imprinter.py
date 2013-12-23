from capuchin.imprinter import Imprinter
from capuchin.imagefeed import ImageFeed

class TestImprinter:

    def setUp(self):
        self.imagefeed = ImageFeed()
        self.imprinter = Imprinter(self.imagefeed)

    def test_imprinter_exists(self):
        assert self.imprinter != None

    def test_imprinter_imprints(self):
        assert self.imprinter.imprint() != None

    def test_imprinter_imagefeed_exists(self):
        assert self.imprinter.imagefeed != None

    def test_imprinter_imagefeed_feeds_images(self):
        assert self.imprinter.imagefeed.feed() != None

