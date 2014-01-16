import numpy
from glimpse.experiment import *
from glimpse.pools import *
from capuchin import *
from config import *

imagefeed = imagefeeds.ImageFeed(IMAGE_LOCATION, FEED_LOCATION)
imprinter = imprinters.Imprinter(imagefeed, INITIAL_LOCATION,
        SORTED_LOCATION, num_prototypes=10)
exp = ExperimentData()
SetModel(exp)
prototypes = imprinter.imprint(exp, initial=True)
exp.extractor.model.s2_kernels = prototypes
ComputeActivation(exp, Layer.S2, MakePool('s'))
TrainAndTestClassifier(exp, Layer.S2)

imagefeed.feed(5)
imprinter.categorize(exp)
before = exp.extractor.model.s2_kernels
new_prototypes = imprinter.imprint(exp)
old_prototypes = exp.extractor.model.s2_kernels
print before
raw_input("ready?")
print old_prototypes

joint_prototypes = [ numpy.concatenate((new_prototypes, old_prototypes)) ]
exp.extractor.model.s2_kernels = prototypes
ComputeActivation(exp, Layer.S2, MakePool('s'))
TrainAndTestClassifier(exp, Layer.S2)


print "Done. You win!"

