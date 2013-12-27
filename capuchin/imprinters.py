import os
from glimpse.experiment import *
from glimpse.models import *
from glimpse.pools import *
from imagefeeds import ImageFeed 

class Imprinter:
    """A simple class that accepts an imagefeed and returns imprinted visual cells from it."""
    
    def __init__(self, imagefeed, sorted_location, initial_image_count, image_package_size, num_prototypes=10):
        self.imagefeed = imagefeed 
        self.sorted_location = sorted_location
        self.num_prototypes = num_prototypes
        self.image_package_size = image_package_size
        self.initial_image_count = initial_image_count
        self.exp = ExperimentData()
        self.pool = MakePool('s')
        self._initial_imprint()
        

    def _initial_imprint(self): 
        self.imagefeed.feed(self.initial_image_count) 
        SetCorpus(self.exp, self.imagefeed.feed_location)
        SetModel(self.exp, model=MakeModel())
        self._imprint() 

    def _imprint(self):
        """Imprints and returns a set of visual cells given a series of images."""
        MakePrototypes(self.exp, self.num_prototypes, algorithm="imprint", pool=self.pool)
        return [ GetPrototype(self.exp, n) for n in range(GetNumPrototypes(self.exp)) ] 
        
    def feed_and_imprint(self):
        """Requests images from this Imprinter's imagefeed and imprints them, returning visual cells."""
        self.imagefeed.feed(self.image_package_size)
        self.categorize()
        return self._imprint()
    
    def categorize(self):
        categories = self._get_categories()
        imagefeed._reset_directory(sorted_location)
        imagefeed._transfer_images(categories, sorted_location)
        
    def _get_categories(self):
        #new_exp = ExperimentData()
        #prototypes = [ GetPrototype(exp, n) for n in range(0, GetNumPrototypes(exp)) ]
        #new_exp.extractor.model.s2_prototypes = prototypes
        SetCorpus(self.exp, self.imagefeed.feed_location) # TODO: INCLUDE PREVIOUS AWESOME PROTOTYPES
        TrainAndTestClassifier(self.exp, self.layers, train_size = 0) # Evaluate without training. But must be trained! 
        preditions = {pred[0] : pred[2] for pred in GetPredictions(self.exp) }
        return predictions



        

