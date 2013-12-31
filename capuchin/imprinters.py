import os
from glimpse.experiment import *
from glimpse.models import *
from glimpse.pools import *
from imagefeeds import ImageFeed 

class Imprinter:
    """A simple class that accepts an imagefeed and returns imprinted visual cells from it."""
    
    def __init__(self, imagefeed, initial_location, sorted_location, 
            initial_image_count, image_package_size, num_prototypes=10):

        self.imagefeed = imagefeed 
        self.initial_location = initial_location
        self.sorted_location = sorted_location
        self.num_prototypes = num_prototypes
        self.image_package_size = image_package_size
        self.initial_image_count = initial_image_count
        self.exp = ExperimentData()
        self.layers = "S2"
        self.pool = MakePool('s')
        
    def imprint(self, exp, initial=False):
        """Imprints and returns a set of visual cells given a series of images."""
        
        if initial:
            count = self.initial_image_count
            corpus = self.initial_location
        else:
            count = self.image_package_size
            corpus = self.sorted_location

        SetCorpus(exp, corpus)
        MakePrototypes(exp, self.num_prototypes, algorithm="imprint", pool=self.pool)
        return exp

    #def get_prototypes(self): 
    #   return [ GetPrototype(self.exp, n) for n in range(GetNumPrototypes(self.exp)) ] 

    def categorize(self, exp):
        categories = self._get_categories(exp)
        self.imagefeed._reset_directory(self.sorted_location)
        self.imagefeed.transfer_images(categories, self.sorted_location, predicted=True)
        
    def _get_categories(self, exp): # This code based off of Mick Thomure's PredictImageClasses gist
        """exp should have a model and prototypes"""

        ev = exp.evaluation[0]
        model = exp.extractor.model
        feed_location = self.imagefeed.feed_location

        image_names = os.listdir(feed_location)
        image_paths = [ os.path.join(feed_location, name) for name in image_names ] 
        images = map(exp.extractor.model.MakeState, image_paths)
        print image_names

        builder = Callback(BuildLayer, model, ev.layers, save_all=False)
        states = self.pool.map(builder, images)
        print states
        features = ExtractFeatures(ev.layers, states)

        labels = ev.results.classifier.predict(features)
        classes = exp.corpus.class_names[labels]

        return dict(zip(image_names, classes)) 



        
        

        
        



        

