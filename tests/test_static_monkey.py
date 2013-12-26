from capuchin.monkeys import StaticMonkey
from capuchin.imprinters import Imprinter
from capuchin.imagefeeds import ImageFeed
from config import *

class TestStaticMonkey():

    def setUp(self):
        self.test_imagefeed = ImageFeed(feed_location=TEST_FEED_LOCATION)
        self.test_static_monkey = StaticMonkey(feed_location=TEST_FEED_LOCATION)

    def test_static_monkey_exists(self):
        assert self.test_static_monkey is not None

    def test_static_monkey_imprinter(self):
        self.test_imagefeed.feed() 
        assert self.test_static_monkey.imprinter.imprint() is not None

    def test_static_monkey_run(self):
        assert self.test_static_monkey.run() is not None


