from capuchin.imagefeeds import ImageFeed
from capuchin.imprinters import Imprinter

imagefeed = ImageFeed("/home/watsonc/capuchin/test/test_corpus", "/home/watsonc/capuchin/test/test_feed")
imprinter = Imprinter(imagefeed, "/home/watsonc/capuchin/test/test_sorted", 2, 1)

imprinter.get_next_prototypes_and_categories()
