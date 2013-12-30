# THIS IS IT!

from capuchin import *
import random

test_window_times = 20
twiddle_imagefeed = capuchin.imagefeeds.ImageFeed(IMAGE_LOCATION, FEED_LOCATION) 
twiddle_imprinter = capuchin.imprinters.Imprinter(twiddle_imagefeed, 
        SORTED_LOCATION, INITIAL_IMAGE_COUNT, IMAGE_PACKAGE_SIZE, NUM_PROTOTYPES) 

def basic():
    monkey = capuchin.monkeys.BasicMonkey(imprinter)
    for n in range(1, test_basic_times): 
        monkey.run()

    return monkey.run()


def twiddle():
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
    monkey = capuchin.monkeys.StaticWindowMonkey(twiddle_imprinter, window)
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

def get_fitness(string)
    monkey = capuchin.monkeys.GeneticMonkey(genetic_imprinter, string) 
    for n in range(1, genetic_time):
        monkey.run()

    return monkey.run()

###################################################################################3

print basic()
print twiddle()
print genetic()
