import os
import shutil
import random
from glimpse.experiment import *
from config import *
from utils import *

class ImageFeed:
    """Feeds images to feed_location to simulate a real-time image feed for Imprinter instances."""

    def __init__(self, image_location, feed_location):
        self.image_location = image_location 
        self.used_images = []
        self.feed_location = feed_location

    def feed(self, reset=True): 
        """Gets IMAGE_PACKAGE_SIZE images from each subdirectory in image_location and return them.""" 
        image_subdirs = get_random_image_sample(IMAGE_PACKAGE_SIZE, self.image_location, self.used_images)
        if reset:
            reset_directory(self.feed_location, self.image_location)
        images = self.move_images(image_subdirs, self.feed_location, folders=True)
        self.used_images.extend(images)
        return image_subdirs 

    def move_images(self, image_subdirs, location, folders=True):
            """Moves images from one directory to another given a dict of subdirectories."""
            image_files = []

            for image in image_subdirs:
                if folders:
                    destination = os.path.join(location, image_subdirs[image], os.path.basename(image)) 
                else:
                    destination = os.path.join(location, os.path.basename(image))

                for subdir in os.listdir(location):
                    image_file = os.path.join(self.image_location, subdir, os.path.basename(image))
                    try: 
                        shutil.copyfile(image_file, destination)
                        break
                    except Exception:
                        pass # We've checked the wrong directory.
                    
                image_files.append(image)

            return image_files 


'''
    def get_categories(self):
        categories = {}
        for subdirectory in os.listdir(self.image_location):
            full_path = os.path.join(self.image_location, subdirectory)
            for image in os.listdir(full_path):
                categories[image] = subdirectory

        return categories
'''

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
                
