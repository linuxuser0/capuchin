import random
from capuchin import *
from config import *

def evaluate_monkey(times, monkey, genetic=False):  
    values = []
    n = 0
    while n < times:
#        print n
        n += monkey.run()
        if n <= times:
            results = try_get_results(monkey)
            values.append(results)
            #print "Round {0}: {1}".format(n, results)

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

    for _ in range(times):
        return monkey.get_results() 
        
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
    print population

    for n in range(times):
        fitnesses = [get_fitness(p[:]) for p in population]
        if max(fitnesses) > all_best_fitness:
            print "NEW BEST SET!"
            all_best_fitness = max(fitnesses)
            all_best = population[fitnesses.index(all_best_fitness)]

        print "ROUND {0}".format(n)
        print population
        print "FITNESSES: {0}".format(fitnesses)

        print "---"

        print "SCREENING"
        population = screen(population, fitnesses)
        if all_best is not None:
            population.append(all_best)
            population.append(all_best)
        print "REPRODUCING"
        population = reproduce(population)

        print "---"
                
    print "ALL TIME BEST: {0}".format(all_best)
    print "FITNESS: {0}".format(all_best_fitness)

def get_initial_population(preset=True, size=4):
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
    
    print population

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

    return random.sample(new_population, 8)
            
def screen(population, fitnesses):
    mapping = zip(population, fitnesses)
    best = sorted(mapping, key=lambda x: x[1])[-4:]
    return map(lambda x: x[0], best)

def get_fitness(string): # modify for average!
    imprinter = get_imprinter()
    monkey = monkeys.GeneticMonkey(imprinter, string) 
    return evaluate_monkey(10, monkey, genetic=True) # ten is number of times to get avg.
'''
def try_test_window(n, tries=0):
    try:
        t = test_window(n)
    except Exception, e:
        error = str(e)
        if "Exp refuses to categorize one class" in error:
            if tries <= MAX_TRIES:
                print "Retrying..."
                print "ISSUE:"
                print error
                tries += 1
                t = try_test_window(n, tries=tries)
            else:
                print "Failed."
                return "FAILURE"
    
    return t
'''

def make_window(window):
    return monkeys.StaticWindowMonkey(get_imprinter(), window)

'''

def evaluate_window(window):
    times = 10
    values = []
    n = 0
    while n < times:
        print "STEP! {0} < 10".format(n)
        t, results = test_window(window)


    average = float(sum(values))/float(len(values))
    print "AVERAGE: {0}".format(average)
    return average 

'''

def test_window(window):
    monkey = make_window(window)
    values = []
    runs = 0
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

    return float(sum(values))/float(len(values))

'''

def try_monkey_run(m, tries=0):
    try:
        n = m.run()
        print "Success!"
    except Exception, e:
        if "Exp refuses to categorize one class" in str(e) or "larger than population":
            if tries <= MAX_TRIES:
                print "Retrying..."
                print str(e)
                tries += 1
                n = try_monkey_run(m, tries=tries)
            else:
                print "Failed."
                return None
        else:
            raise
    return n 

'''

###################################################################################

points = []
for n in range(5, 10): #61
    print "TESTING NUM_PROTOTYPES {0}".format(n)
    b = basic(10, n)
    print b
    points.append(b)

average = float(sum(points))/float(len(points)) 
print "FINAL VALUE: {0}".format(average)

#for _ in range(0, 20):
#    print "TWIDDLE {0}".format(_)
#    twiddle(50, 10)
'''
for n in range(2, 61): 
    t = test_window(n)
    print "Round {0}: {1}".format(n, t)
'''    
#twiddle(10, 2) 
#genetic(5)
