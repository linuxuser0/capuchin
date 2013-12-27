import os
from glimpse.experiment import *
from glimpse.models import *
from glimpse.pools import *
from imagefeeds import ImageFeed 

class Imprinter:
    """A simple class that accepts an imagefeed and returns imprinted visual cells from it."""
    
    CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    DEFAULT_FEED_LOCATION= os.path.join(CURRENT_DIRECTORY, "data", "feed")

    def __init__(self, imagefeed, initial_image_count=2):
        self.imagefeed = imagefeed 
        self.initial_image_count = initial_image_count
        self.exp = ExperimentData()
        self.pool = MakePool('s')
        self._initial_imprint()
        

    def _initial_imprint(self):
        self.imagefeed.feed(self.initial_image_count) 
        SetCorpus(self.exp, self.imagefeed.feed_location)
        SetModel(self.exp, model=MakeModel())
        self.imprint() 
                

    def imprint(self):
        """Imprints and returns a set of visual cells given a series of images."""
        MakePrototypes(self.exp, num_prototypes=10, algorithm="imprint", pool=self.pool)
        return [ GetPrototype(self.exp, n) for n in range(GetNumPrototypes(self.exp)) ] 
        
    def feed_and_imprint(self):
        """Requests images from this Imprinter's imagefeed and imprints them, returning visual cells."""
        self.imagefeed.feed()
        return self.imprint()



        

