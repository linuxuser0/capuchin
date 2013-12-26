import os
import shutil
import random

class ImageFeed:
    """Feeds images to feed_location to simulate a real-time image feed for Imprinter instances."""
    CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    DEFAULT_IMAGE_LOCATION = os.path.join(CURRENT_DIRECTORY, "data", "corpus")
    ACCEPTED_FILETYPES = ['.png', '.jpg', '.jpeg']

    def __init__(self, image_location=DEFAULT_IMAGE_LOCATION, feed_location=None):
        self.image_location = image_location 
        self.used_images = []
        self.feed_location = feed_location

    def train(self, exp, fraction):
        pass

    def feed(self, image_package_size=10): #TODO: make unsupervised
        """Get image_package_size images from each subdirectory in image_location and return them.""" 

        self._reset_feed()

        image_subdirs = self._get_random_image_sample(image_package_size)
        image_files = []

        for image in image_subdirs:
            image_file = os.path.join(self.image_location, image_subdirs[image], image) 
            destination = os.path.join(self.feed_location, image_subdirs[image], image)
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
        
        for subdirectory in unused_images: 
            subdir_images = random.sample(unused_images[subdirectory], size) 
            for image in subdir_images: 
                images[image] = subdirectory

        return images

    def _reset_feed(self):
        shutil.rmtree(self.feed_location)
        os.makedirs(self.feed_location)
        for subdir in os.listdir(self.image_location):
            full_path = os.path.join(self.feed_location, subdir)
            os.makedirs(full_path)



