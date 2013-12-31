from glimpse.experiment import *
from glimpse.pools import *

exp = ExperimentData()
SetModel(exp)
# unsure of below
SetCorpus(exp, "test_sorted")
MakePrototypes(exp, 1, 'imprint')
# unsure of above
print "almost there"
ComputeActivation(exp, Layer.S2, MakePool('s'))
print "just have to train."
TrainAndTestClassifier(exp, Layer.S2)
print "done."

print exp.extractor.model.s2_prototypes
