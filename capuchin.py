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
            print "Round {0}: {1}".format(n, results)

    average = float(sum(values))/float(len(values))
    print "AVERAGE: {0}".format(average)
    return average 

def try_get_results(monkey, final=False):
    try: 
        return monkey.get_results(final)
    except IndexError: # implying faulty GA code
        return 0

def get_imprinter(): 
    return imprinters.Imprinter(get_imagefeed(), INITIAL_LOCATION, SORTED_LOCATION, num_prototypes=NUM_PROTOTYPES) 

def get_imagefeed():
    return imagefeeds.ImageFeed(IMAGE_LOCATION, FEED_LOCATION) 

def basic(times, num_prototypes): 
    imprinter = get_imprinter()
    monkey = monkeys.BasicMonkey(imprinter, IMAGE_PACKAGE_SIZE, num_prototypes=num_prototypes)
    return evaluate_monkey(times, monkey)
        
def twiddle(max_size, delta): # Algorithm introduced by Sebastian Thrun (genius) on Udacity - thanks!
    print "Begin twiddle."
    window = random.randint(1, max_size) 
    best_accuracy = test_window(window)

    while delta > 1:
        print "Delta and window:"
        print delta
        print window
        window += delta 
        accuracy = test_window(window)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            delta = int(delta * 1.1)
        else:
            window -= 2*delta
            accuracy = test_window(window)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                delta = int(delta * 1.1)
            else:
                # cry for mercy
                window += delta
                delta = int(delta * 0.9)

    return window, best_accuracy

def test_window(window): 
    times = 10
    monkey = monkeys.StaticWindowMonkey(get_imprinter(), window) 
    return evaluate_monkey(times, monkey) 


def genetic(times): 
    """Optimizes the instructions for GeneticMonkey."""
    population = get_initial_population()
    all_best = None
    all_best_fitness = -1

    for n in range(times):
        population = reproduce(population)
        population = screen(population)
        fitnesses = map(get_fitness, population)
        if max(fitnesses) > all_best_fitness:
            all_best_fitness = max(fitnesses)
            all_best = population[fitness.index(all_best_fitness)]

    print all_best
    print all_best_fitness

def get_initial_population():
    """Returns a list of strings of instructions."""
    population_size = 10
    instructions_per = 10
    population = []
    for p in range(population_size): 
        instructions = []
        for i in range(instructions_per):
            keywords = ["rf", "rl", "af", "al", "no"]
            key = random.choice(keywords)
            value = random.randint(1, 5) # fine tune for results 
            instructions.append("{0} {1}".format(key, value))
        population.append(instructions)

    return population


    return 
def reproduce(population):
    """Reproduces the instruction strings randomly, via genetic algorithm."""
    new_population = []

    for a in population:
        for b in population:
            child = []
            for n in range(0, len(a)):
                child.append(random.choice([a, b])[n])

            new_population.append(child)

    return random.sample(new_population, 100)
            
def screen(population):
    return sorted(population, key=get_fitness)[-10:]

def get_fitness(string): # modify for average!
    imprinter = get_imprinter()
    monkey = monkeys.GeneticMonkey(imprinter, string) 
    return evaluate_monkey(10, monkey, genetic=True) # ten is number of times to get avg.
        

###################################################################################
"""
points = []
for n in [50]:
    print "TESTING NUM_PROTOTYPES {0}".format(n)
    points.append(basic(10, n))

average = float(sum(points))/float(len(points)) 
print "FINAL VALUE: {0}".format(average)
"""

#for _ in range(0, 20):
#    print "TWIDDLE {0}".format(_)
#    twiddle(50, 10)

"""
for n in range(1, 61):
    t = test_window(n)
    print n
    print t
"""    
    
#twiddle(10, 2) 
genetic(2)
