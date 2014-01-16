import time
from trainer import *

si = get_sorted_imagefeed()
for _ in range(10):
    print "Feed."
    si.feed()
    time.sleep(1000)

print "Done."
    

