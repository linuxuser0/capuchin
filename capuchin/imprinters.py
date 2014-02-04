import os, numpy, copy
from glimpse.experiment import *
from glimpse.models import *
from glimpse.pools import *
from imagefeeds import ImageFeed 
from utils import *
from config import *

class Imprinter:
    """A simple class that accepts an imagefeed and returns imprinted visual cells from it."""
    
    def __init__(self, imagefeed, initial_location, sorted_location, num_prototypes=10):
        self.imagefeed = imagefeed 
        self.initial_location = initial_location
        self.sorted_location = sorted_location
        self.num_prototypes = num_prototypes
        self.exp = ExperimentData()
        self.layers = "S2"
        self.pool = MakePool('s')
        
    def imprint(self, prototypes=None, initial=False, num_prototypes=None):
        """Imprints and returns a set of visual cells given a series of images."""
        num_prototypes = self.num_prototypes if num_prototypes is None else num_prototypes
        corpus = self.initial_location if initial else self.sorted_location 
        exp = make_exp(prototypes, corpus=corpus)

        MakePrototypes(exp, num_prototypes, algorithm="imprint", pool=MakePool('s'))
        return get_prototypes(exp)

    def categorize(self, protos):
        """Given a set of prototypes, moves images from feed_location into categories in self.sorted_location"""
        mask = ChooseTrainingSet(get_labels(corpus=FEED_LOCATION), train_size=0.5)
        categories = classify_images(protos, get_images(mask=mask), get_labels(mask=mask), get_images(mask=~mask))
        reset_directory(self.sorted_location, self.imagefeed.image_location)
        self.imagefeed.move_images(categories, self.sorted_location)
