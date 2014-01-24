import copy
import numpy
import glob
from imprinters import Imprinter
from imagefeeds import ImageFeed
from glimpse.pools import *
from glimpse.experiment import *
from utils import *

"""A collection of classes which utilize Imprinter instances to dynamically adapt HMAX models."""

class BasicMonkey:
    """Uses initial imprinting to evaluate images. Rather simple."""
    def __init__(self, imprinter, num_prototypes):
        self.imprinter = imprinter
        self.num_prototypes = num_prototypes
        self.pool = MakePool('s') 
        self.protos = self.imprinter.imprint(initial=True, num_prototypes=num_prototypes)

    def run(self):
        self.imprinter.imagefeed.feed()
        return 1 # number of feeds used

    def get_results(self):
        if self.protos is None or len(self.protos) == 0:
            return 0.0
        else:
            return test_prototypes(self.protos)

    def get_new_prototypes(self, protos, reset=True, images=5, num=10, n=0):
        if protos is None or len(protos) == 0:
            return protos 
        try:
            self.imprinter.imagefeed.feed(reset=reset) 
            self.imprinter.categorize(protos)
            new_protos = self.imprinter.imprint(prototypes=protos, num_prototypes=num)

        except Exception, e:
            if self.feeds >= self.remaining:
                raise Exception, "Out of remaining feeds." 
            
            if "No images found in directory" in str(e) or "Need at least two examples of class" in str(e):
                if n == 2:
                    raise Exception, "Exp refuses to categorize one class"
                else:
                    new_protos = self.get_new_prototypes(protos, reset=False, n=(n+1)) 
                    self.feeds += 1
            else: 
                raise

        return new_protos[0] 

class StaticWindowMonkey(BasicMonkey): 
    
    def __init__(self, imprinter, window_size=None): 
        self.imprinter = imprinter 
        self.window_size = window_size
        self.pool = MakePool('s')
        self.protos = self.imprinter.imprint(initial=True, num_prototypes=10)
       
    def run(self, remaining=100): 
        self.remaining = remaining
        self.feeds = 1 # typical reset

        try:
            new_prototypes = self.get_new_prototypes(self.protos, 10)
        except Exception, e:
            if "remaining feeds" in str(e):
                return self.remaining
            elif "refuses" in str(e):
                return 3 
            else:
                raise

        prototypes = [ new_prototypes + self.protos[0] ] 
        if self.window_size is not None and len(prototypes) > self.window_size:
            prototypes = prototypes[-self.window_size:] 

        self.protos = prototypes

        print "Done."
        return self.feeds 

       
class GeneticMonkey(BasicMonkey):  

    def __init__(self, imprinter, instructions):
        self.imprinter = imprinter
        self.pool = MakePool('s')
        self.instructions = instructions
        self.protos = self.imprinter.imprint(initial=True, num_prototypes=10)
                
    def run(self, remaining):
        self.remaining = remaining
        self.feeds = 1
        keyword, argument = self.instructions.pop(0).split()
        times = int(argument) 
       
        if self.protos is not None and len(self.protos) != 0:
            if keyword == "rf":
                for n in range(times):
                    if len(self.protos) > 0:
                        self.protos.pop(0)
            elif keyword == "rl":
                for n in range(times):
                    if len(self.protos) > 0:
                        self.protos.pop()
            elif keyword == "af":
                try:
                    new_prototypes = self.get_new_prototypes(self.protos, 10)
                except Exception, e:
                    if "remaining feeds" in str(e):
                        return self.remaining
                    elif "refuses" in str(e):
                        return 3 
                    else:
                        raise

                if new_prototypes is not None:
                    self.protos = [ new_prototypes + self.protos[0] ] 
                    

            elif keyword == "al":
                try:
                    new_prototypes = self.get_new_prototypes(self.protos, 10)
                except Exception, e:
                    if "remaining feeds" in str(e):
                        return self.remaining
                    elif "refuses" in str(e):
                        return 3 
                    else:
                        raise

                if new_prototypes is not None:
                    self.protos = [ self.protos[0] + new_prototypes ] 

            return self.feeds

        return self.remaining

