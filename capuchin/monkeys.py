import numpy
import glob
from imprinters import Imprinter
from imagefeeds import ImageFeed
from glimpse.pools import *
from glimpse.experiment import *

"""A collection of classes which utilize Imprinter instances to dynamically adapt HMAX models."""

class BasicMonkey:

    """Uses initial imprinting to evaluate images. Rather dumb."""

    def __init__(self, imprinter, image_package_size):
        self.imprinter = imprinter
        self.image_package_size = image_package_size
        self.pool = MakePool('s')
        self.exp = self.make_exp(initial=True)

    def run(self):
        self.imprinter.imagefeed.feed(self.image_package_size) 

    def get_results(self, final=False): # Based on Mick Thomure's code TODO understand

        exp = self.exp

        ev = exp.evaluation[0]
        model = exp.extractor.model

        if final:
            loc = self.imprinter.imagefeed.image_location
            image_files = []
            for subdir in os.listdir(loc):
                image_names = os.listdir(os.path.join(loc, subdir))
                image_files.extend([os.path.join(loc, subdir, name) for name in image_names])
        else:
            loc = self.imprinter.imagefeed.feed_location 
            image_names = os.listdir(loc)
            image_files = [os.path.join(loc, name) for name in image_names]
                    
        images = map(model.MakeState, image_files) 
        builder = Callback(BuildLayer, model, ev.layers, save_all=False)
        states = self.pool.map(builder, images)

        features = ExtractFeatures(ev.layers, states)
        labels = ev.results.classifier.predict(features)
        classes = dict(zip(image_names, exp.corpus.class_names[labels]))

        actual = self.imprinter.imagefeed.get_categories()

        correct = 0
        count = len(classes)

        for image_name in classes:
            if classes[image_name] == actual[image_name]:
                correct += 1 

        return float(correct)/float(count)
    
    def make_exp(self, initial=False, imprint=True, prototypes=None): 
        exp = ExperimentData()
        SetModel(exp)
        if prototypes is None:
            prototypes = self.imprinter.imprint(exp, initial=initial) 
            # TODO try multiple times when not initial?
        else:
            SetCorpus(exp) # FIX THIS LINE
        exp = self.set_prototypes(exp, prototypes) 

        return exp

    def make_testing_exp(self, prototypes):
        exp = ExperimentData()
        SetModel(exp)
        self.set_prototypes(exp, prototypes)
        return exp

    def set_prototypes(self, exp, prototypes):
        exp.extractor.model.s2_kernels = prototypes
        ComputeActivation(exp, Layer.S2, self.pool)
        TrainAndTestClassifier(exp, Layer.S2)
        return exp



class StaticWindowMonkey(BasicMonkey): 
    
    def __init__(self, imprinter, window_size=None): 
        self.imprinter = imprinter 
        self.window_size = window_size
        self.pool = MakePool('s')
        self.exp = self.make_exp(initial=True)
        self.feeds = 1 
                
    def run(self): 

        prototypes = [ numpy.concatenate(self.get_new_prototypes(self.exp) + self.get_prototypes(self.exp)) ]

        if self.window_size is not None and len(prototypes) > self.window_size:
            numpy.delete(prototypes, numpy.s_[3:])

        self.exp = self.make_exp(prototypes)

        print "Done."

        return self.feeds

    def get_prototypes(self, exp):
        return exp.extractor.model.s2_kernels

    def get_new_prototypes(self, exp, images=5, reset=True):
        try:
            self.imprinter.imagefeed.feed(images, reset) 
            self.imprinter.categorize(exp)
            new_exp = self.imprinter.imprint(exp)

        except Exception, e:
            if "No images found in directory" in str(e):
                new_exp = self.get_new_prototypes(exp, reset=False) 
                print "Timestep skipped." # TODO implement in test 
                self.feeds += 1
            else: 
                raise 

        return new_exp 

       
class GeneticMonkey(BasicMonkey):

    def __init__(self, imprinter, instructions):
        self.imprinter = imprinter
        self.instructions = instructions
        self.prototypes = imprinter.get_prototypes()
        
    def run(self):
        keyword, argument = self.instructions.pop(0).split()
        times = int(argument)
        new_prototypes, categories = self.imprinter.get_next_prototypes_and_categories()
        
        if keyword == "rf":
            for n in range(0, times):
                self.prototypes.pop(0)
        elif keyword == "rl":
            for n in range(0, times):
                self.prototypes.pop()
        elif keyword == "af":
            for n in range(0, times):
                self.prototypes[:0] = new_prototypes
        elif keyword == "al":
            for n in range(0, times):
                self.prototypes.extend(new_prototypes)

        return _evaluate_prototypes(exp, self.prototypes, categories)

            
        
        

