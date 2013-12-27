from imprinters import Imprinter
from imagefeeds import ImageFeed

"""A collection of classes which utilize Imprinter instances to dynamically adapt HMAX models."""

class StaticMonkey:
    
    DEFAULT_WINDOW_SIZE = 5

    def __init__(self, imprinter): 
        self.imprinter = imprinter 
        
    def run(self):
        """Imprint using self.imprinter and record results and resultant visual cells, returning results."""

        
         
