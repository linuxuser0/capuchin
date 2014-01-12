import copy
import numpy
import glob
from imprinters import Imprinter
from imagefeeds import ImageFeed
from glimpse.pools import *
from glimpse.experiment import *

"""A collection of classes which utilize Imprinter instances to dynamically adapt HMAX models."""

class BasicMonkey:

    """Uses initial imprinting to evaluate images. Rather dumb."""

    def __init__(self, imprinter, image_package_size, num_prototypes): # for testing, i_p_s = 5
        self.imprinter = imprinter
        self.image_package_size = image_package_size
        self.num_prototypes = num_prototypes
        self.pool = MakePool('s') 
        self.exp = self.make_exp(initial=True, num_prototypes=num_prototypes)

    def run(self):
        self.imprinter.imagefeed.feed(self.image_package_size) 
        return 1 # number of feeds used

    def get_results(self, final=False): # Based on Mick Thomure's code - thanks! 

#        print "GETTING RESULTS!"

        exp = self.exp

        #print self.get_prototypes(self.exp)

        ev = exp.evaluation[0]
        model = exp.extractor.model

        #if final:
        #    loc = self.imprinter.imagefeed.image_location
        #    image_files = []
        #    for subdir in os.listdir(loc):
        #        image_names = os.listdir(os.path.join(loc, subdir))
        #        image_files.extend([os.path.join(loc, subdir, name) for name in image_names])
        #else:
        loc = self.imprinter.imagefeed.feed_location 
        image_names = os.listdir(loc)
        image_files = [os.path.join(loc, name) for name in image_names]
        
        #print len(image_files)
                    
#        print "BUILDING IMAGES"
#       
        images = map(model.MakeState, image_files) 
        builder = Callback(BuildLayer, model, ev.layers, save_all=False)
        states = self.pool.map(builder, images)

#        print "CATEGORIZING!"

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
    
    def make_exp(self, initial=False, imprint=True, prototypes=None, num_prototypes=10): 
        exp = ExperimentData()
        SetModel(exp)
        if prototypes is not None:
            SetCorpus(exp, self.imprinter.sorted_location)
        else:
            prototypes = self.imprinter.imprint(exp, initial=initial, num_prototypes=num_prototypes) 

        exp = self.set_prototypes(exp, prototypes, initial=initial) 

        return exp

    def make_testing_exp(self, prototypes):
        exp = ExperimentData()
        SetModel(exp)
        self.set_prototypes(exp, prototypes)
        return exp

    def set_prototypes(self, exp, prototypes, initial=False):
        #if not initial:
        #    SetCorpus(exp, self.imprinter.sorted_location)
        exp.extractor.model.s2_kernels = prototypes
        ComputeActivation(exp, Layer.S2, self.pool)
        TrainAndTestClassifier(exp, Layer.S2)
        return exp

    def get_prototypes(self, exp):
        return exp.extractor.model.s2_kernels[0]

    def get_new_prototypes(self, exp, images=5, reset=True, num=10, n=0):
        print "Getting new prototypes..."
        try:
            print "Feeding..."
            self.imprinter.imagefeed.feed(images, reset=reset) 
            print "Categorizing..."
            self.imprinter.categorize(exp)
            print "Imprinting..."
            prototypes = self.imprinter.imprint(exp, num_prototypes=num)

        except Exception, e:
            if self.feeds >= self.remaining:
                raise Exception, "Out of remaining feeds." 
            
            if "No images found in directory" in str(e) or "Need at least two examples of class" in str(e):
                print "Reattempting prototypes"
                print str(e)
                if n == 3:
                    print "Not reattempting..."
                    raise Exception, "Exp refuses to categorize one class"
                prototypes = self.get_new_prototypes(exp, reset=False, n=(n+1)) 
                #print "Timestep skipped."
                self.feeds += 1
            else: 
                raise

        print "Completed."
        return prototypes[0] 

class StaticWindowMonkey(BasicMonkey): 
    
    def __init__(self, imprinter, window_size=None): 
        self.imprinter = imprinter 
        self.window_size = window_size
        self.pool = MakePool('s')
        self.exp = self.make_exp(initial=True)
                
    def run(self, remaining=100): 
        self.remaining = remaining
        self.feeds = 1 # typical reset

        try:
            new_prototypes = self.get_new_prototypes(self.exp)
        except Exception, e:
            if "remaining feeds" in str(e):
                return self.remaining
            else:
                raise
            
        current_prototypes = self.get_prototypes(self.exp)
        prototypes = [ new_prototypes + current_prototypes ] 
        if self.window_size is not None and len(prototypes) > self.window_size:
            prototypes = prototypes[-self.window_size:] 

        self.exp = self.set_prototypes(self.exp, prototypes)

        print "Done."
        print self.feeds
        return self.feeds 

       
class GeneticMonkey(BasicMonkey):  

    def __init__(self, imprinter, instructions):
        self.imprinter = imprinter
        self.pool = MakePool('s')
        self.instructions = instructions
        self.exp = self.make_exp(initial=True)
                
    def run(self):
#        print "RUNNING!"
        
        self.feeds = 1
        keyword, argument = self.instructions.pop(0).split()
        times = int(argument) 
        prototypes = self.get_prototypes(self.exp) 
        
        if keyword == "rf":
            for n in range(times):
                if len(prototypes) > 0:
                    prototypes.pop(0)
        elif keyword == "rl":
            for n in range(times):
                if len(prototypes) > 0:
                    prototypes.pop()
        elif keyword == "af":
            try:
                new_prototypes = self.get_new_prototypes(self.exp, num=times)
                if new_prototypes is not None:
                    prototypes = [ numpy.concatenate((new_prototypes, prototypes)) ] # TODO REPLACE WITH ABOVE SYNTAX
            except:
                pass
        elif keyword == "al":
            try:
                new_prototypes = self.get_new_prototypes(self.exp, num=times)
                if new_prototypes is not None:
                    prototypes = [ numpy.concatenate((prototypes, new_prototypes)) ]
            except:
                pass

#        print "SETTING PROTOTYPES!"
        try:
            self.exp = self.set_prototypes(self.exp, prototypes) # put in DOR - that if this fails, will revert to old prototype results 
        except:
            pass

        return self.feeds


            
        
        

