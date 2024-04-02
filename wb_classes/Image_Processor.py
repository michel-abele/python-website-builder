import json
import os
import shutil

class Image_Processor:
    def __init__(self, source_path, target_path):
        self.source_path = source_path
        self.target_path = target_path
        self.image_links_file = "./temp/image_links.json"

    # ==============================================================================================
    # process images
    def process_images(self):

        with open(self.image_links_file, 'r') as f:
            image_links = json.load(f)

        unique_image_links = list(set(image_links))

        for link in unique_image_links:
            source_file_path = os.path.join(self.source_path, link)
            target_file_path = os.path.join(self.target_path, link)

            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
            shutil.copy2(source_file_path, target_file_path)
