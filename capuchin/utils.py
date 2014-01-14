from glimpse.experiment import *
from glimpse.models import *
from glimpse.pools import *
# functions below based off of Mick Thomure's code - thanks!

TEST_SORTED = "test/test_sorted"

def make_exp(protos, corpus=None):
    exp = ExperimentData()
    SetModel(exp)
    if corpus:
        SetCorpus(exp, corpus)
    return exp


def test_prototypes(protos): # FIX FOR TEST_FEED
    # Assumes images are in test_feed.
    mask = ChooseTrainingSet(get_labels(corpus=TEST_SORTED), train_size=0.5)
    predictions = classify_images(protos, get_images(mask=mask), get_labels(mask=mask))
    return get_accuracy(predictions, get_image_labels(mask=~mask))


def get_accuracy(pred, act):
    correct = 0
    for a in zip(pred, act):
        if a[0] == a[1]:
            correct += 1

    return float(correct)/float(len(pred))


def classify_images(protos, images, labels): # make use right classifier size when called to categorize! PUT IN OBSERVATIONS
    model = make_model(protos)
    clf = train_classifier(model, images, labels)
    labels = clf.predict(get_features(images, model))
    classes = get_class_names(labels) 
    return dict(zip(images, classes))


def train_classifier(model, images, labels): 
    return FitClassifier(get_features(images, model), labels) 


def get_labels(mask=None, corpus=TEST_SORTED):
    exp = ExperimentData()
    SetCorpus(exp, corpus)
    if mask is not None:
        return exp.corpus.labels[mask]
    else:
        return exp.corpus.labels


def get_images(mask=None, corpus=TEST_SORTED):
    exp = ExperimentData()
    SetCorpus(exp, corpus)
    if mask is not None:
        return exp.corpus.paths[mask]
    else:
        return exp.corpus.paths


def get_image_labels(mask, corpus=TEST_SORTED):
    return dict(zip(get_images(mask), get_labels(mask)))


def get_features(images, model):
    pool = MakePool()
    images = map(model.MakeState, images)
    builder = Callback(BuildLayer, model, model.LayerClass.S2, save_all=False)
    states = pool.map(builder, images)
    features = ExtractFeatures(model.LayerClass.S2, states)
    return features

def get_class_names(labels, corpus=TEST_SORTED):
    exp = ExperimentData()
    SetCorpus(exp, corpus)
    return exp.corpus.class_names[labels]

def make_model(protos):
    model = Model()
    if isinstance(protos, list):
        model.s2_kernels = protos
    else:
        model.s2_kernels = [protos]
    return model


def get_classes(model, images):
    pool = MakePool()
    images = map(model.MakeState, paths)
    builder = Callback(BuildLayer, model, model.LayerClass.S2, save_all=False)
    states = self.pool.map(builder, images)
    features = ExtractFeatures(model.LayerClass.S2, states)
    
