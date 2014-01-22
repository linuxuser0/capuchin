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
        corpus = self.initial_location if initial else self.imagefeed.feed_location
        exp = make_exp(prototypes, corpus=corpus)

        MakePrototypes(exp, num_prototypes, algorithm="imprint", pool=MakePool('s'))
        return self.get_prototypes(exp)

    def get_prototypes(self, exp): 
       return exp.extractor.model.s2_kernels

    def categorize(self, protos):
        mask = ChooseTrainingSet(get_labels(corpus=FEED_LOCATION), train_size=0.5)
        categories = classify_images(protos, get_images(mask=mask), get_labels(mask=mask), get_images(mask=~mask))
        self.imagefeed._reset_directory(self.sorted_location)
        self.imagefeed.transfer_images(categories, self.sorted_location)
       
    def _get_categories(self, exp): # This code based off of Mick Thomure's PredictImageClasses gist
        """exp should have a model and prototypes"""

        ev = exp.evaluation[0]
        model = exp.extractor.model
        feed_location = self.imagefeed.feed_location

        image_names = os.listdir(feed_location)
        image_paths = [ os.path.join(feed_location, name) for name in image_names ] 
        images = map(exp.extractor.model.MakeState, image_paths)

        builder = Callback(BuildLayer, model, ev.layers, save_all=False)
        states = self.pool.map(builder, images)
        features = ExtractFeatures(ev.layers, states)

        labels = ev.results.classifier.predict(features)
        classes = exp.corpus.class_names[labels]

        return dict(zip(image_names, classes)) 



        
        

        
        



        

