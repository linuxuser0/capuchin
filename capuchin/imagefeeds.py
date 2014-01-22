import os
import shutil
import random
from config import *
from glimpse.experiment import *

class ImageFeed:
    """Feeds images to feed_location to simulate a real-time image feed for Imprinter instances."""

    ACCEPTED_FILETYPES = ['.png', '.jpg', '.jpeg']

    def __init__(self, image_location, feed_location):
        self.image_location = image_location 
        self.used_images = []
        self.feed_location = feed_location

    def feed(self, reset=True): 
        """Get image_package_size images from each subdirectory in image_location and return them.""" 
        image_subdirs = self._get_random_image_sample(IMAGE_PACKAGE_SIZE)
        images = self.transfer_images(image_subdirs, self.feed_location, folders=True, reset=reset) 
        return image_subdirs 


class SortedImageFeed(ImageFeed):

    def __init__(self, image_location, feed_location):
        self.image_location = image_location
        self.image_locations = [ os.path.join(image_location, loc) for loc in sorted(os.listdir(image_location)) ]
        self.used_images = [] # to be compatible with "legacy" code
        self.used_locations = []
        self.feed_location = feed_location

    def feed(self, reset=True):
        location = self.image_locations.pop(0)
        subdirs = os.listdir(location) 
        if reset:
            shutil.rmtree(self.feed_location)
            os.makedirs(self.feed_location)
            for subdir in subdirs:
                original = os.path.join(location, subdir)
                destination = os.path.join(self.feed_location, subdir)
                shutil.copytree(original, destination) 
        else:
            for subdir in subdirs:
                original = os.path.join(location, subdir)
                fullpath = os.path.join(location, subdir)
                destination = os.path.join(self.feed_location, subdir)
                for image in os.listdir(original):
                    imagepath = os.path.join(fullpath, image)
                    shutil.copy(imagepath, destination)
                
