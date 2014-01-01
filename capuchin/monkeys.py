import numpy
import glob
from imprinters import Imprinter
from imagefeeds import ImageFeed
from glimpse.pools import *
from glimpse.experiment import *

"""A collection of classes which utilize Imprinter instances to dynamically adapt HMAX models."""

class BasicMonkey:

    """Uses initial imprinting to evaluate images. Rather dumb."""

    def __init__(self, imprinter):
        self.imprinter = imprinter
        self.pool = MakePool('s')
        self.prototypes = imprinter.get_prototypes()
        print "ENSURE THIS ISN'T NONE: %s" % self.prototypes

    def run(self):
        new_prototypes, categories = self.imprinter.get_next_prototypes_and_categories()
        _evaluate_prototypes(self.prototypes, categories, self.pool) 
        

    def get_results(self, final=False): # Based on Mick Thomure's code TODO understand

        if final:
            prototypes = self.exp.extractor.model.s2_kernels   

            exp = self.make_testing_exp(prototypes) 
            ev = exp.evaluation[0]
            model = exp.extractor.model

            image_names = glob.glob(self.testing_location)
            images = map(model.MakeState, image_names) 
            builder = Callback(BuildLayer, model, ev.layers, save_all=False)
            states = self.pool.map(builder, images)

            features = ExtractFeatures(ev.layers, states)
            labels = ev.results.classifier.predict(features)
            classes = dict(zip(image_names, exp.corpus.class_names[labels]))
        else:
            predictions = GetPredictions(self.exp)
            classes = dict(zip(predictions[0], predictions[2]))
        
        actual = self.imprinter.imagefeed.get_categories()

        correct = 0
        count = len(classes)

        for image_name in image_names:
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

    def set_prototypes(self, exp, prototypes):
        exp.extractor.model.s2_kernels = prototypes
        ComputeActivation(exp, Layer.S2, self.pool)
        TrainAndTestClassifier(exp, Layer.S2)
        return exp

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

            
        
        

