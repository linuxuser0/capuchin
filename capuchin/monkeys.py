import numpy
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
        

    def evaluate_prototypes(self, prototypes, categories, pool):
        exp = ExperimentData()
        exp.extractor.model.s2_prototypes = prototypes
        ComputeActivation(exp, "S2", pool)
        TrainAndTestClassifier(exp, "S2")
        predictions = { pred[0] : pred[2] for pred in GetPredictions(exp) }
        actual = categories # TODO original datasets - make so doesn't influence ImageFeed categories (get from src.)

        correct = 0
        count = len(predictions)

        for key, value in predictions:
            if actual[key] == value:
                correct += 1

        return float(correct)/float(count)



class StaticWindowMonkey(BasicMonkey): 
    
    def __init__(self, imprinter, window_size=None): 
        self.imprinter = imprinter 
        self.window_size = window_size
        self.pool = MakePool('s')
        self.exp = self.make_exp(imprinter, initial=True)
                
    def run(self): 
        self.imprinter.imagefeed.feed(1) # TODO change to variable
        categories = self.imprinter.categorize(self.exp) #obsoletes the old get_new_prototypes_and_categories
        new_prototypes = self.imprinter.imprint() # so does this      
        prototypes = numpy.concatenate((new_prototypes, self.prototypes))

        if window_size is not None and len(self.prototypes) > window_size:
            prototypes.pop()

        self.exp = make_exp(prototypes)
        
    def make_exp(self, imprinter, initial=False): # add to BasicMonkey
        exp = ExperimentData()
        SetModel(exp)
        imprinter.imprint(exp, initial)
        ComputeActivation(exp, Layer.S2, self.pool)
        TrainAndTestClassifier(exp, Layer.S2)
        return exp
        
        
        
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

            
        
        

