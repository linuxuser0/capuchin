import re
f = open('nontwiddle_Test2')

for line in f.readlines():
    if re.search("AVERAGE", line) is not None:
        print line

