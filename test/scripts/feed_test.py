import os
import time
from trainer import *

si = get_sorted_imagefeed()
for _ in range(10):
    print "Feed."
    si.feed()
    print "RESULTS==="
    print os.listdir("../test_feed")
    time.sleep(5)

print "Done."
    

