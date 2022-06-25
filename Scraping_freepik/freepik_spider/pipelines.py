# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

# Renaming the images
class FreepikSpiderPipeline(object): 
    def process_item(self, item, spider):
        # Path
        os.chdir("D:/Github_shared_projects/projects_shared/Python")

        if item['images'][0]['path']:
            # The current name of the image comes from path
            # example of 'path':'full/25fc1e57eec5509108274de134a3100b5e43af8b.jpg'
            # Building the new name for the image
            new_name = 'freepik_' + item['image_id'][0] + '.jpg'
            new_image_path = 'full/' + new_name
            # Renaming the old name with the created new one
            os.rename(item['images'][0]['path'], new_image_path)
            return item

