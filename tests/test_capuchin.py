from capuchin.capuchin.capuchin import Capuchin
from capuchin.capuchin.imprinter import Imprinter
from capuchin.capuchin.imagefeed import ImageFeed

class TestCapuchin():

    def setUp(self):
        self.test_imagefeed = ImageFeed()
        self.test_imprinter = Imprinter()
        self.test_capuchin = Capuchin()

    def test_capuchin_exists(self):
        assert self.test_capuchin != None

    def test_capuchin_imprinter(self):
        test_images = self.test_imagefeed.feed() 
        assert self.test_capuchin.imprinter.imprint(test_images) != None

    def test_capuchin_run(self):
        assert self.test_capuchin.run() != None


