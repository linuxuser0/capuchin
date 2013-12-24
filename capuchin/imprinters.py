import os
from glimpse.experiment import *
from imagefeeds import ImageFeed 

class Imprinter:
    """A simple class that accepts an imagefeed and returns imprinted visual cells from it."""
    
    CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    DEFAULT_FEED_LOCATION= os.path.join(CURRENT_DIRECTORY, "data", "feed")

    def __init__(self, imagefeed=ImageFeed(), feed_location=DEFAULT_FEED_LOCATION):
        self.imagefeed = imagefeed 
        self.imagefeed.feed_location = feed_location
        self.exp = ExperimentData()
        SetCorpus(self.exp, feed_location)

    def imprint(self):
        """Imprints and returns a set of visual cells given a series of images."""
        MakePrototypes(self.exp, num_prototypes=10, algorithm="imprint")
        return [ GetPrototype(self.exp, n) for n in range(GetNumPrototypes(self.exp)) ] 
        
    def feed_and_imprint(self):
        """Requests images from this Imprinter's imagefeed and imprints them, returning visual cells."""
        print self.imagefeed.feed_location
        self.imagefeed.feed()
        return self.imprint()



        

