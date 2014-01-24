from capuchin.utils import *
from capuchin.imagefeeds import * 
from capuchin.imprinters import *
from capuchin.monkeys import *

'''
PROTOTYPES = range(2, 21)
WINDOWS = range(4, 61, 4)
NUM_TRIALS = 5 
GENERATIONS = 5 
'''

PROTOTYPES = range(2, 5)
WINDOWS = range(2, 5)
NUM_TRIALS = 2 
GENERATIONS = 1

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
                runs += monkey.run()
                points.append(monkey.get_results())
                print points[-1]
            except Exception, e:
                if "sample" in str(e):
                    print_and_log("Imprinter swap.")
                    monkey.imprinter = get_imprinter(imagefeed_getter())
                else:
                    raise

            #print "Run {0} finished".format(runs)

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
    monkey = monkeys.GeneticMonkey(imprinter, string)
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

# CHECK double_test(test_baseline, PROTOTYPES)
double_test(test_window, WINDOWS)
test_genetic(GENERATIONS, get_imagefeed, False)
print_and_log("--------------------------------------------")
test_genetic(GENERATIONS, get_imagefeed, True)
print_and_log("--------------------------------------------")
test_genetic(GENERATIONS, get_sorted_imagefeed, False)
print_and_log("--------------------------------------------")
test_genetic(GENERATIONS, get_sorted_imagefeed, True)

