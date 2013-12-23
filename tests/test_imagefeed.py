from capuchin.imagefeed import ImageFeed

class TestImageFeed:
    
    def setUp(self):
        self.imagefeed = ImageFeed()

    def test_imagefeed_exists(self):
        assert self.imagefeed != None

    def test_imagefeed_feeds(self):
        assert self.imagefeed.feed() != None


