import os, random

class ImageFeed:
    """Feeds images to Imprinter instances to simulate a real-time image feed."""
    CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    DEFAULT_IMAGE_LOCATION = os.path.join(CURRENT_DIRECTORY, "data")
    DEFAULT_DEFAULT_IMAGE_PACKAGE_SIZE = 10
    ACCEPTED_FILETYPES = ['.png', '.jpg', '.jpeg']

    def __init__(self, image_location=DEFAULT_IMAGE_LOCATION, default_image_package_size=
            DEFAULT_DEFAULT_IMAGE_PACKAGE_SIZE):
        self.image_location = image_location 
        self.default_image_package_size = default_image_package_size
        self.used_images = []

    def feed(self, image_package_size=None):
        """Get image_package_size images from each subdirectory in image_location and return them.""" 
        if image_package_size is None:
            image_package_size = self.default_image_package_size

        image_names = self._get_random_image_sample(image_package_size)
        image_files = [ os.path.join(self.image_location, name) for name in image_names ]
        self.used_images.extend(image_names)
        return image_files
    
    def _get_unused_images(self):
        """Get a list of all available images which haven't been used."""
        subdirectories = os.listdir(self.image_location)
        unused_images = []
        
        for subdirectory in subdirectories: 
            full_subdirectory_path = os.path.join(self.image_location, subdirectory)
            all_files = os.listdir(full_subdirectory_path)
            all_images = [ image for image in all_files if os.path.splitext(image)[1].lower() in self.ACCEPTED_FILETYPES ]
            subdir_unused_images = [ image for image in all_images if image not in self.used_images ]
            unused_images.append(subdir_unused_images)

        return unused_images

    def _get_random_image_sample(self, size):
        """Gets a random sample of images of size from each subdirectory in image_location."""
        images = []
        for subdirectory in self._get_unused_images():
            images.extend(random.sample(subdirectory, size))

        return images


