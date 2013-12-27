import numpy
from imprinters import Imprinter
from imagefeeds import ImageFeed

"""A collection of classes which utilize Imprinter instances to dynamically adapt HMAX models."""

class StaticMonkey:
    
    def __init__(self, imprinter): 
        self.imprinter = imprinter 
        self.prototypes = None 
        
    def run(self): 
        new_prototypes = self.imprinter.feed_and_imprint() 
        if self.prototypes is None:
            self.prototypes = new_prototypes
        else:
            self.prototypes = numpy.concatenate((self.prototypes, new_prototypes))
        return self.prototypes
        
         
