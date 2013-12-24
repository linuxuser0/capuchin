from imprinters import Imprinter

"""A collection of classes which utilize Imprinter instances to dynamically adapt HMAX models."""

class StaticMonkey:
    
    DEFAULT_WINDOW_SIZE = 5

    def __init__(self, window_size = DEFAULT_WINDOW_SIZE):
        self.imagefeed = ImageFeed()
        self.imprinter = Imprinter(self.imagefeed)
        self.prototypes = None
        

    def run(self):
        """Imprint using self.imprinter and record results and resultant visual cells, returning results."""
         
