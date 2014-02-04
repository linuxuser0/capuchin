import random
import os, shutil
from glimpse.experiment import *
from glimpse.models import *
from glimpse.pools import *
from config import * 


# functions below based off of Mick Thomure's code - thanks!

pool = MakePool()

def make_exp(protos, corpus=None): # CHECK
    exp = ExperimentData()
    SetModel(exp)
    if corpus:
        SetCorpus(exp, corpus)
    return exp


def test_prototypes(protos): # CHECK 
    # Assumes images are in test_feed.
    mask = ChooseTrainingSet(get_labels(corpus=FEED_LOCATION), train_size=0.5)
    predictions = classify_images(protos, get_images(mask=mask), get_labels(mask=mask), get_images(mask=~mask))
    actual = dict(zip(get_images(~mask), get_class_names(get_labels(~mask))))
    return get_accuracy(predictions, actual) 


def get_accuracy(pred, act): # CHECK
    correct = 0
    for key in pred.keys():
        if pred[key] == act[key]:
            correct += 1

    return float(correct)/float(len(pred))


def classify_images(protos, train_images, train_labels, test_images): # CHECK 
    model = make_model(protos)
    clf = train_classifier(model, train_images, train_labels)
    labels = clf.predict(get_features(test_images, model))
    classes = get_class_names(labels) 
    return dict(zip(test_images, classes))


def train_classifier(model, images, labels): # CHECK
    return FitClassifier(get_features(images, model), labels) 


def get_labels(mask=None, corpus=FEED_LOCATION): # CHECK
    exp = ExperimentData()
    SetCorpus(exp, corpus)
    if mask is not None:
        return exp.corpus.labels[mask]
    else:
        return exp.corpus.labels

def get_images(mask=None, corpus=FEED_LOCATION): # CHECK
    exp = ExperimentData()
    SetCorpus(exp, corpus)
    if mask is not None:
        return exp.corpus.paths[mask]
    else:
        return exp.corpus.paths


def get_image_labels(mask, corpus=FEED_LOCATION): # CHECK
    return dict(zip(get_images(mask), get_labels(mask)))


def get_features(images, model): # CHECK
    images = map(model.MakeState, images)
    builder = Callback(BuildLayer, model, model.LayerClass.C2, save_all=False)
    states = pool.map(builder, images)
    features = ExtractFeatures(model.LayerClass.C2, states)
    return features

def get_class_names(labels, corpus=FEED_LOCATION): # CHECK
    exp = ExperimentData()
    SetCorpus(exp, corpus)
    return exp.corpus.class_names[labels]

def make_model(protos): # CHECK
    model = Model()
    if isinstance(protos, list):
        model.s2_kernels = protos
    else:
        model.s2_kernels = [protos]
    return model


def get_classes(model, images): # CHECK 
    images = map(model.MakeState, paths)
    builder = Callback(BuildLayer, model, model.LayerClass.C2, save_all=False)
    states = pool.map(builder, images)
    features = ExtractFeatures(model.LayerClass.C2, states)

############################# IMAGEFEED #############################


def get_unused_images(image_location, used_images): # CHECK
    """Get a dictionary of all available images which haven't been used."""
    subdirectories = os.listdir(image_location)
    unused_images = {} 
    
    for subdirectory in subdirectories: 
        full_subdirectory_path = os.path.join(image_location, subdirectory)
        all_files = os.listdir(full_subdirectory_path)
        all_images = [ image for image in all_files if os.path.splitext(image)[1].lower() in ACCEPTED_FILETYPES ]
        subdir_unused_images = [ image for image in all_images if image not in used_images ]
        unused_images[subdirectory] = subdir_unused_images

    return unused_images

def get_random_image_sample(size, image_location, used_images): # CHECK
    """Gets a random sample of images of size from each subdirectory in image_location, returning a dictionary."""
    images = {}
    unused_images = get_unused_images(image_location, used_images) 
    
    for subdirectory in unused_images: 
        subdir_images = random.sample(unused_images[subdirectory], size) 
        for image in subdir_images:
            images[image] = subdirectory 

    return images

def reset_directory(directory, image_location, folders=True): # CHECK 
    try:
        shutil.rmtree(directory)
    except OSError:
        pass

    os.makedirs(directory)
    if folders:
        for subdir in os.listdir(image_location):
            full_path = os.path.join(directory, subdir)
            os.makedirs(full_path)
'''
def get_predictions(exp, location): # CHECK
    SetCorpus(exp, location)  
    raw_predictions = GetPredictions(exp)
    predictions = {pred[0] : pred[2] for pred in raw_predictions}
    return predictions
'''

#################### MONKEYS ######################

def get_prototypes(exp):
    return exp.extractor.model.s2_kernels[0]

##################### TRAINER ##################### ALL BELOW CHECK ###################

def evaluate_monkey(times, monkey, genetic=False):  
    values = []
    n = 0
    while n < times:
        n += monkey.run()
        if n <= times:
            results = try_get_results(monkey)
            values.append(results)

    average = float(sum(values))/float(len(values))
    return average 

def try_get_results(monkey, final=False):
    try: 
        return monkey.get_results(final)
    except IndexError: # implying faulty GA code
        return 0

def get_imprinter(imagefeed): 
    return imprinters.Imprinter(imagefeed, INITIAL_LOCATION, SORTED_LOCATION, num_prototypes=NUM_PROTOTYPES) 

def basic(times, num_prototypes): 
    imprinter = get_imprinter()
    monkey = monkeys.BasicMonkey(imprinter, IMAGE_PACKAGE_SIZE, num_prototypes=num_prototypes)
    data = []
    for _ in range(times):
        monkey.run()
        m = monkey.get_results()
        data.append(m)

    average = float(sum(data))/float(len(data))
    return average

def test_window(window): 
    times = 10 
    monkey = monkeys.StaticWindowMonkey(get_imprinter(), window) 
    return evaluate_monkey(times, monkey) 


def genetic(times): 
    """Optimizes the instructions for GeneticMonkey."""
    population = get_initial_population()
    all_best = None
    all_best_fitness = -1
    print population

    for n in range(times):
        fitnesses = [get_fitness(p[:]) for p in population]
        if max(fitnesses) > all_best_fitness:
            all_best_fitness = max(fitnesses)
            all_best = population[fitnesses.index(all_best_fitness)]

        population = screen(population, fitnesses)
        if all_best is not None:
            population.append(all_best)
            population.append(all_best)
        population = reproduce(population)

    print "ALL TIME BEST: {0}".format(all_best)
    print "FITNESS: {0}".format(all_best_fitness)

def get_initial_population(preset=True, size=3):
    """Returns a list of strings of instructions."""
    if not preset:
        instructions_per = 10
        population = []
        for p in range(size): 
            instructions = []
            for i in range(instructions_per):
                keywords = ["rf", "rl", "af", "al", "no"]
                key = random.choice(keywords)
                value = random.randint(1, 5) # fine tune for results 
                instructions.append("{0} {1}".format(key, value))
            population.append(instructions)
    else:
        population =[ ['no 1'] * 10, ['al 1'] * 9 + ['rf 2'], ['af 1'] * 8 + ['rl 1'] * 2, 
                get_initial_population(preset=False, size=1)[0] ]
    
    return population


def reproduce(population):
    """Reproduces the instruction strings randomly, via genetic algorithm."""
    new_population = []

    for a in population:
        for b in population:
            child = []
            for n in range(0, len(a)):
                child.append(random.choice([a, b])[n])

            new_population.append(child)

    return random.sample(new_population, 6)
            
def screen(population, fitnesses):
    mapping = zip(population, fitnesses)
    best = sorted(mapping, key=lambda x: x[1])[-3:]
    return map(lambda x: x[0], best)

def get_fitness(string): # modify for average!
    imprinter = get_imprinter()
    monkey = monkeys.GeneticMonkey(imprinter, string) 
    values = []
    runs = 0
    while runs < 10:
        try:
            runs += monkey.run(remaining=(10-runs))
            values.append(monkey.get_results())
        except Exception, e:
            if "sample" in str(e):
                print "Imprinter - swapped."
                monkey.imprinter = get_imprinter()
            else:
                raise

    return float(sum(values))/float(len(values))

def make_window(window):
    return monkeys.StaticWindowMonkey(get_imprinter(), window)

def test_window(window):
    monkey = make_window(window)
    values = []
    runs = 0
    print monkey.get_results()
    while runs < 10:
        print "Run {0} begun.".format(runs)
        try:
            print "Running!"
            runs += monkey.run(remaining=(10-runs))
            print "Obtaining results."
            values.append(monkey.get_results())
        except Exception, e:
            error = str(e)
            if "sample" in error:
                print "Imprinter - swapped."
                monkey.imprinter = get_imprinter()
            else:
                raise

    return float(sum(values))/float(len(values))

def print_and_log(text):
    print text
    with open("final_output.log", "a") as f:
        f.write(str(text) + "\n")

def get_sorted_imagefeed():
    return SortedImageFeed(SORTED_IMAGE_LOCATION, FEED_LOCATION)

def get_imagefeed():
    return ImageFeed(IMAGE_LOCATION, FEED_LOCATION) 

def get_imprinter(imagefeed): 
    return Imprinter(imagefeed, INITIAL_LOCATION, SORTED_LOCATION, num_prototypes=NUM_PROTOTYPES) 

####################################################################################################################

def test_baseline(imagefeed_getter, num_prototypes):
    points = []
    for trial in range(NUM_TRIALS):
        for _ in range(10):
            imagefeed = imagefeed_getter()
            imprinter = get_imprinter(imagefeed)
            monkey = BasicMonkey(imprinter, num_prototypes=num_prototypes)  
            monkey.run()
            points.append(monkey.get_results())
            #print "Run {0} finished.".format(_)

        print_and_log("Trial {0}/{1} finished for {2}/{3} prototypes.".format(trial, NUM_TRIALS, num_prototypes, len(PROTOTYPES)))

    return sum(points)/float(len(points))

def test_window(imagefeed_getter, window_size):
    points = []
    for trial in range(NUM_TRIALS): 
        runs = 0
        imagefeed = imagefeed_getter()
        imprinter = get_imprinter(imagefeed)
        monkey = StaticWindowMonkey(imprinter, window_size)
        while runs < 10:
            try:
                remaining = 10 - runs
                runs += monkey.run(remaining)
                points.append(monkey.get_results())
                print_and_log(points[-1])
                print "runs: {0}".format(runs)
            except Exception, e:
                if "sample" in str(e):
                    print_and_log("Imprinter swap.")
                    monkey.imprinter = get_imprinter(imagefeed_getter())
                else:
                    raise

            print "Run {0} finished".format(runs)

        print_and_log("Trial {0}/{1} finished for window size {2}/{3}.".format(trial, NUM_TRIALS, window_size, len(WINDOWS)))
        print_and_log("RESULTS: {0}".format(sum(points)/float(len(points))))

    return sum(points)/float(len(points))

def test_genetic(generations, imagefeed_getter, preset):
    population = get_initial_population(preset)    
    best = (None, -1)
    for _ in range(generations):
        print_and_log("Getting fitnesses for generation {0}".format(_))
        fitnesses = [get_fitness(p[:], imagefeed_getter) for p in population]
        if max(fitnesses) > best[1]:
            best_fitness = max(fitnesses)
            best_species = dict(zip(fitnesses, population))[best_fitness]
            best = (best_species, best_fitness)

        population = screen(population, fitnesses) 
        if best[0] is not None: 
            population.append(best[0])
        population = reproduce(population)
        print_and_log("Population: {0} at generation {1}".format(population, _))
        print_and_log("with fitnesses {0}".format(fitnesses))

    print_and_log("{0} => {1}".format(best[0], best[1]))

def get_fitness(string, imagefeed_getter):
    imprinter = get_imprinter(imagefeed_getter())
    monkey = GeneticMonkey(imprinter, string)
    values = []
    runs = 0
    for _ in range(NUM_TRIALS):
        while runs < 10:
            #print "Run {0} begins!".format(runs)
            try:
                runs += monkey.run(remaining=(10-runs))
                values.append(monkey.get_results())
            except Exception, e:
                if "sample" in str(e):
                    print_and_log("Imprinter swap.")
                    monkey.imprinter = get_imprinter(imagefeed_getter())
                else:
                    raise

        return sum(values)/float(len(values))


def double_test(tester, values):
    points = []
    for num in values:
        points.append(tester(get_imagefeed, num))
        print_and_log("Finished {0}: {1}".format(num, points[-1]))

    print_and_log("Points: {0}".format(points))
    print_and_log("AVERAGE: {0}".format(sum(points)/float(len(points))))

    print_and_log("----------------------------------------------")
    print "PART B"

    points = []
    for num in values:
        points.append(tester(get_sorted_imagefeed, num))

    print_and_log(points)
    print_and_log(sum(points)/float(len(points)))

    print_and_log("---------------------------------------------")

def single_test(tester, values):
    points = []
    for num in values:
        points.append(tester(get_sorted_imagefeed, num))

    print_and_log(points)
    print_and_log(sum(points)/float(len(points)))

    print_and_log("---------------------------------------------")


