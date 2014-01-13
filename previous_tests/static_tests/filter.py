f = open('static_test', 'r')
for line in f.readlines():
    if "Round" in line:
        print line
