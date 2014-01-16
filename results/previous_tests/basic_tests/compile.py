files = ['basic_test', 'basic_test2', 'basic_test3', 'basic_test4']

for f in files:
    lines = []
    f = open(f, 'rw')
    for line in f.readlines():
        
