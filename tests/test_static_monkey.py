from capuchin.monkeys import StaticMonkey
from capuchin.imprinters import Imprinter
from capuchin.imagefeeds import ImageFeed

class TestStaticMonkey():

    def setUp(self):
        self.test_imagefeed = ImageFeed()
        self.test_imprinter = Imprinter()
        self.test_static_monkey = StaticMonkey()

    def test_static_monkey_exists(self):
        assert self.test_static_monkey is not None

    def test_static_monkey_imprinter(self):
        test_images = self.test_imagefeed.feed() 
        assert self.test_static_monkey.imprinter.imprint(test_images) is not None

    def test_static_monkey_run(self):
        assert self.test_static_monkey.run() is not None


