# THIS IS IT!

import random
from capuchin import *
from config import *

test_window_times = 20
imagefeed = imagefeeds.ImageFeed(IMAGE_LOCATION, FEED_LOCATION) 
imprinter = imprinters.Imprinter(imagefeed, INITIAL_LOCATION, SORTED_LOCATION, num_prototypes=NUM_PROTOTYPES) 

def basic(times):
    values = []
    monkey = monkeys.BasicMonkey(imprinter, IMAGE_PACKAGE_SIZE)
    for n in range(times): 
        monkey.run()
        if n == times:
            results = monkey.get_results(final=True)
        else:
            results = monkey.get_results()
        values.append(results)
        print "Round {0}: {1}".format(n+1, results)

    print "AVERAGE: {0}".format(float(sum(values))/float(len(values)))

def twiddle(): # Algorithm introduced by Sebastian Thrun (genius) on Udacity - thanks!
    window = random.randint(1, 1000)  
    delta = 50
    best_accuracy = test_window(window)

    while delta > 1:
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
    monkey = monkeys.StaticWindowMonkey(twiddle_imprinter, window) 
    for n in range(1, test_window_times):
        monkey.run()

    return monkey.run()

def genetic(times):
    population = get_initial_population()
    for n in range(0, times):
        population = reproduce(population)
        population = screen(population)

    return max(population, key=get_fitness)

def reproduce(population):
    new_population = []

    for a in population:
        for b in population:
            child = []
            for n in range(0, len(a)):
                child.append(random.choice([a, b])[n])

            new_population.append(child)
            
def screen(population):
    return sorted(population, key=get_fitness)[-10:]

def get_fitness(string):
    monkey = capuchin.monkeys.GeneticMonkey(genetic_imprinter, string) 
    for n in range(1, genetic_time):
        monkey.run()

    return monkey.run()

###################################################################################3

basic(5)
#print twiddle()
#print genetic()
