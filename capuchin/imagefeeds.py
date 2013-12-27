import os
import shutil
import random

from glimpse.experiment import *

class ImageFeed:
    """Feeds images to feed_location to simulate a real-time image feed for Imprinter instances."""

    ACCEPTED_FILETYPES = ['.png', '.jpg', '.jpeg']

    def __init__(self, image_location, root_feed_location):
        self.image_location = image_location 
        self.used_images = []
        self.feed_location = os.path.join(root_feed_location, "feed")

    def feed(self, image_package_size): 
        """Get image_package_size images from each subdirectory in image_location and return them.""" 
        self._reset_directory(self.feed_location)
        image_subdirs = self._get_random_image_sample(image_package_size)
        images = self._transfer_images(image_subdirs, self.feed_location) 
        return images 

            
    def _transfer_images(self, image_subdirs, location):
        image_files = []
        self._reset_directory(location)

        for image in image_subdirs:
            image_file = os.path.join(self.image_location, image_subdirs[image], image) 
            destination = os.path.join(location, image_subdirs[image], image) 
            print "IMAGE: %s. DESTINATION: %s" % (image_file, destination)
            shutil.copyfile(image_file, destination)

            self.used_images.append(image)
            image_files.append(image)
        
        return image_files


    def _get_unused_images(self):
        """Get a dictionary of all available images which haven't been used."""
        subdirectories = os.listdir(self.image_location)
        unused_images = {} 
        
        for subdirectory in subdirectories: 
            full_subdirectory_path = os.path.join(self.image_location, subdirectory)
            all_files = os.listdir(full_subdirectory_path)
            all_images = [ image for image in all_files if os.path.splitext(image)[1].lower() in self.ACCEPTED_FILETYPES ]
            subdir_unused_images = [ image for image in all_images if image not in self.used_images ]
            unused_images[subdirectory] = subdir_unused_images

        return unused_images

    def _get_random_image_sample(self, size):
        """Gets a random sample of images of size from each subdirectory in image_location, returning a dictionary."""
        images = {}
        unused_images = self._get_unused_images()

        print unused_images
        
        for subdirectory in unused_images: 
            subdir_images = random.sample(unused_images[subdirectory], size) 
            for image in subdir_images:
                images[image] = subdirectory 

        return images

    def _reset_directory(self, directory):
        try:
            shutil.rmtree(directory)
        except OSError:
            pass
        os.makedirs(directory)
        for subdir in os.listdir(self.image_location):
            full_path = os.path.join(directory, subdir)
            os.makedirs(full_path)

    def _get_predictions(self, exp, location):
        print exp
        SetCorpus(exp, location)  
        raw_predictions = GetPredictions(exp)
        predictions = {pred[0] : pred[2] for pred in raw_predictions}
        print predictions
        return predictions


