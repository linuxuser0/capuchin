import random
from capuchin import *
from config import *

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

def get_sorted_imagefeed():
    return imagefeeds.SortedImageFeed(SORTED_IMAGE_LOCATION, FEED_LOCATION)

def get_imagefeed():
    return imagefeeds.ImageFeed(IMAGE_LOCATION, FEED_LOCATION) 

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
