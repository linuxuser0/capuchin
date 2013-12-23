from imagefeed import ImageFeed 

class Imprinter:
    def __init__(self, imagefeed=ImageFeed()):
        self.imagefeed = imagefeed 

    def imprint(self, images):
        """Imprints and returns a set of visual cells given a series of images."""
        pass

    
    def feed_and_imprint(self):
        """Requests images from this Imprinter's imagefeed and imprints them, returning visual cells."""
        return self.imprint(self.imagefeed.feed())
