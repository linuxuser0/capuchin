from capuchin.capuchin.imagefeed import ImageFeed

class TestImageFeed:
    
    def setUp(self):
        self.imagefeed = ImageFeed()

    def test_imagefeed_exists(self):
        assert self.imagefeed != None

    def test_imagefeed_get_unused_images(self):
        assert self.imagefeed._get_unused_images() is not None

    def test_imagefeed_feeds(self):
        assert self.imagefeed.feed() is not None


