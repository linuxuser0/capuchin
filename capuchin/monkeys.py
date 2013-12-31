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
        

    def get_results(self, prototypes): # Based on Mick Thomure's code
        
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

        print classes
        
        actual = self.imprinter.imagefeed.get_categories()

        print actual

        correct = 0
        count = len(classes)

        for image_name in image_names:
            if classes[image_name] == actual[image_name]:
                correct += 1 

        return float(correct)/float(count)
    
    def make_exp(self, imprinter, initial=False): # add to BasicMonkey
        exp = ExperimentData()
        SetModel(exp)
        imprinter.imprint(exp, initial)
        ComputeActivation(exp, Layer.S2, self.pool)
        TrainAndTestClassifier(exp, Layer.S2)
        return exp

 


class StaticWindowMonkey(BasicMonkey): 
    
    def __init__(self, imprinter, window_size=None): 
        self.imprinter = imprinter 
        self.window_size = window_size
        self.pool = MakePool('s')
        self.exp = self.make_exp(imprinter, initial=True)
                
    def run(self): 
        print "Run initialized."
         
        print self.get_new_prototypes()[0].shape
        print self.get_prototypes(self.exp)[0].shape

        prototypes = self.get_new_prototypes() + self.get_prototypes(self.exp)

        if self.window_size is not None and len(prototypes) > self.window_size:
            prototypes.pop()

        print self.get_new_prototypes()[0].shape
        print self.get_prototypes(self.exp)[0].shape

        print "CREATING FINAL MAGIC:"

        self.exp = self.make_exp(self.imprinter)
    
        self.exp.extractor.model.s2_kernels = prototypes 

        print "Done."

    def get_prototypes(self, exp):
        return exp.extractor.model.s2_kernels

    def get_new_prototypes(self):
        try:
            self.imprinter.imagefeed.feed(5) # TODO change to variable
            self.imprinter.categorize(self.exp) #obsoletes the old get_new_prototypes_and_categories
            new_prototypes = self.imprinter.imprint(self.exp) # so does this      
        except Exception, e:
            if "No images found in directory" in str(e):
                new_prototypes = self.get_new_prototypes() # images from one or more labels missing, retry
            else: 
                raise 

        return new_prototypes

       
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

            
        
        

