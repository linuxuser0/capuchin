from trainer import *
from capuchin.monkeys import *

PROTOTYPES = range(2, 51)
WINDOWS = range(2, 61)
NUM_TRIALS = 20 

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
            monkey = StaticMonkey(imprinter, window_size) # TODO FIX DEF
            runs += monkey.run()
            points.append(monkey.get_results())
            print "Run {0} finished".format(runs)

        print "Trial {0} finished.".format(trial)

    return sum(points/float(len(points))
        

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

double_test(test_baseline, PROTOTYPES)
double_test(test_window, WINDOWS)

