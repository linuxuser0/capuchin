from trainer import *
from capuchin.monkeys import *

PROTOTYPES = range(2, 3)
WINDOWS = range(2, 3)
NUM_TRIALS = 2#0 
GENERATIONS = 1

def test_baseline(imagefeed_getter, num_prototypes):
    points = []
    for trial in range(NUM_TRIALS):
        for _ in range(10):
            imagefeed = imagefeed_getter()
            imprinter = get_imprinter(imagefeed)
            monkey = BasicMonkey(imprinter, num_prototypes=num_prototypes)  
            monkey.run()
            points.append(monkey.get_results())
            print "Run {0} finished.".format(_)

        print "Trial {0} finished.".format(trial)

    return sum(points)/float(len(points))

def test_window(imagefeed_getter, window_size):
    points = []
    for trial in range(NUM_TRIALS): 
        runs = 0
        while runs < 10:
            imagefeed = imagefeed_getter()
            imprinter = get_imprinter(imagefeed)
            monkey = StaticWindowMonkey(imprinter, window_size)
            try:
                runs += monkey.run()
                points.append(monkey.get_results())
            except Exception, e:
                if "sample" in error:
                    print "Imprinter swap."
                    monkey.imprinter = get_imprinter(imagefeed_getter())
                else:
                    raise

            print "Run {0} finished".format(runs)

        print "Trial {0} finished.".format(trial)

    return sum(points/float(len(points)))

def test_genetic(generations, imagefeed_getter, preset):
    population = get_initial_population(preset)    
    best = (None, -1)
    for _ in range(generations):
        fitnesses = [get_fitness(p[:], imagefeed_getter) for p in population]
        if max(fitnesses) > all_best[1]:
            best_fitness = max(fitnesses)
            best_species = dict(zip(fitnesses, population))[best_fitness]
            best = (best_species, best_fitness)

        population = screen(population, fitnesses) 
        if best[0] is not None: 
            population.append(best[0])
        population = reproduce(population)

    print "{0} => {1}".format(best[0], best[1])

def get_fitness(string, imagefeed_getter):
    impritner = get_imprinter(imagefeed_getter())
    monkey = monkeys.GeneticMonkey(imprinter, string)
    values = []
    runs = 0
    while runs < 10:
        print "Run {0} begins!".format(runs)
        try:
            runs += monkey.run(remaining=(10-runs))
            values.append(monkey.get_results())
        except Exception, e:
            if sample in str(e):
                print "Imprinter swap."
                monkey.imprinter = get_imprinter(imagefeed_getter())
            else:
                raise

    return sum(values)/float(len(values))


def double_test(tester, values):
    points = []
    for num in values:
        points.append(tester(get_imagefeed, num))
        print "Finished {0}:".format(num)

    print points
    print sum(points)/float(len(points))

    print "----------------------------------------------"

    points = []
    for num in values:
        points.append(tester(get_sorted_imagefeed, num))

    print points
    print sum(points)/float(len(points))

    print "---------------------------------------------"

#CHECK double_test(test_baseline, PROTOTYPES)
double_test(test_window, WINDOWS)
test_genetic(GENERATIONS)


