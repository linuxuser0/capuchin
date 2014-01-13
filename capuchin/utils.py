from glimpse.experiment import *
from glimpse.models import *
from glimpse.pools import *
# functions below based off of Mick Thomure's code - thanks!

TEST_FEED = "test/test_feed"
LAYER = Layer.C2

def test_prototypes(protos):
    # Assumes images are in test_feed.
    mask = ChooseTrainingSet(labels, train_size=0.5)
    predictions = classify_images(protos, get_images(mask))
    return get_accuracy(predictions, get_image_labels(~mask))


def get_accuracy(pred, act):
    correct = 0
    for a in zip(pred, act):
        if a[0] == a[1]:
            correct += 1

    return float(correct)/float(len(pred))


def classify_images(protos, images):
    model = make_model(protos)
    pool = MakePool()
    clf = train_classifier(model, pool, images)
    labels = clf.predict(get_features(images=images))
    classes = get_class_names(labels) 
    return dict(zip(images, classes))


def train_classifier(model, pool, images): 
    return FitClassifier(get_features(images=images), get_labels()) 


def get_labels(corpus=TEST_FEED):
    exp = ExperimentData()
    SetCorpus(exp, corpus)
    return exp.corpus.labels[mask]


def get_images(mask, corpus=TEST_FEED):
    exp = ExperimentData()
    SetCorpus(exp, corpus)
    return exp.corpus.paths[mask]


def get_image_labels(mask, corpus=TEST_FEED):
    return dict(zip(get_images(mask), get_labels(mask)))


def get_features(images=None, corpus=TEST_FEED):
    images = images if images is not None else get_images(corpus) 
    images = map(model.MakeState, images)
    builder = Callback(BuildLayer, model, LAYER, save_all=False)
    states = pool.map(builder, images)
    features = ExtractFeatures(layer, states)

def get_class_names(labels, corpus=TEST_FEED):
    exp = ExperimentData()
    SetCorpus(exp, corpus)
    return exp.corpus.class_names[labels]
    

def make_model(protos):
    model = Model()
    model.s2_kernels = [protos]
    return model


def get_classes(model, images):
    images = map(model.MakeState, paths)
    builder = Callback(BuildLayer, model, ev.layers, save_all=False)
    states = self.pool.map(builder, images)
    features = ExtractFeatures(ev.layers, states)
    
