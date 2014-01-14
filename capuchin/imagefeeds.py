import os
import shutil
import random

from glimpse.experiment import *

class ImageFeed:
    """Feeds images to feed_location to simulate a real-time image feed for Imprinter instances."""

    ACCEPTED_FILETYPES = ['.png', '.jpg', '.jpeg']

    def __init__(self, image_location, feed_location):
        self.image_location = image_location 
        self.used_images = []
        self.feed_location = feed_location

    def feed(self, image_package_size, reset=True): 
        """Get image_package_size images from each subdirectory in image_location and return them.""" 
        print "FED LIKE A CAT"
        image_subdirs = self._get_random_image_sample(image_package_size)
        images = self.transfer_images(image_subdirs, self.feed_location, folders=True, reset=reset) 
        return image_subdirs 

            
    def transfer_images(self, image_subdirs, location, folders=True, predicted=False, reset=True):
        image_files = []
        if reset:
            #print "CLEARING {0}".format(location)
            self._reset_directory(location, folders)

        #print "TRANFERING to {0}".format(location)

        for image in image_subdirs:

            if folders:
                destination = os.path.join(location, image_subdirs[image], image) 
            else:
                destination = os.path.join(location, image)
             
            if predicted:
                for subdir in os.listdir(location):
                    image_file = os.path.join(self.image_location, subdir, image)
                    try: 
                        shutil.copyfile(image_file, destination)
                        break
                    except Exception:
                        pass

            else:
                image_file = os.path.join(self.image_location, image_subdirs[image], image) 
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

        #print unused_images

        return unused_images
    
    def _get_all_images(self):
        images = {}
        subdirectories = os.listdir(self.image_location)

        for subdirectory in subdirectories:
            full_subdirectory_path = os.path.join(self.image_location, subdirectory)
            all_files = os.listdir(full_subdirectory_path)
            all_images = [ image for image in all_files if os.path.splitext(image)[1].lower() in self.ACCEPTED_FILETYPES ]
            images[subdirectory] = all_images      

        return images

    def _get_random_image_sample(self, size):
        """Gets a random sample of images of size from each subdirectory in image_location, returning a dictionary."""
        images = {}
        unused_images = self._get_unused_images() 
        
        for subdirectory in unused_images: 
            subdir_images = random.sample(unused_images[subdirectory], size) 
            for image in subdir_images:
                images[image] = subdirectory 

        return images

    def get_categories(self):
        categories = {}
        for subdirectory in os.listdir(self.image_location):
            full_path = os.path.join(self.image_location, subdirectory)
            for image in os.listdir(full_path):
                categories[image] = subdirectory

        return categories
            

    def _reset_directory(self, directory, folders=True):
        try:
            shutil.rmtree(directory)
        except OSError:
            pass

        #print "DIRECTORY {0} DELETED".format(directory)
        #print "FOLDERS: {0}".format(folders)

        os.makedirs(directory)
        if folders:
            for subdir in os.listdir(self.image_location):
                full_path = os.path.join(directory, subdir)
                os.makedirs(full_path)


    def _get_predictions(self, exp, location):
        SetCorpus(exp, location)  
        raw_predictions = GetPredictions(exp)
        predictions = {pred[0] : pred[2] for pred in raw_predictions}
        return predictions


