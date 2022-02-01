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
    
        # Path to be updated
        os.chdir("D:/_DSTI_/Python Project/_Scrapy_portraits/freepik_spider/Freepik_images")

        if item['images'][0]['path']:
            new_name = 'freepik_' + item['image_id'][0] + '.jpg'
            new_image_path = 'full/' + new_name
            os.rename(item['images'][0]['path'], new_image_path)
            return item

