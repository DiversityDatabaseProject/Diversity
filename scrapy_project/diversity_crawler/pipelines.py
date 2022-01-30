# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os, csv

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.loader import ItemLoader
from .items import DiversityCrawlerItem

class DiversityCrawlerPipeline:
    def process_item(self, item, spider):
        return item

class DataWriterPipeline(object):
    writer=None
    def __init__(self):
        if os.path.isdir('csv'):
            pass
        else:
            os.makedirs('csv')

    def process_item(self, item, spider):
        if self.writer==None:
            self.writer = csv.writer(open('csv/'+item['folder']+'.csv', 'w'))
            self.writer.writerow(['host','search_key','filename','url','ethnicity','description','img_type'])
        
        #loader = ItemLoader (product)
        #self.writer.writerow([item_loader.get_output_value('host'),item_loader.get_output_value('search_key'),item_loader.get_output_value('filename'),item_loader.get_output_value('img_url'),item_loader.get_output_value('ethnicity'),item_loader.get_output_value('description'),item_loader.get_output_value('img_type')])
        self.writer.writerow([item['host'],item['search_key'],item['filename'],item['img_urls'],item['ethnicity'],item['description'],item['img_type']])
        return item

class LastPagePipeline(object):
    writer=None
    def __init__(self):
        if os.path.isdir('data'):
            pass
        else:
            os.makedirs('data')

    def process_item(self, item, spider):
        #if self.writer==None:
        self.writer = csv.writer(open('data/next_page.csv', 'w'))
        self.writer.writerow([item['last_page']])
        return item

class ImagesDownloadPipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename','')

    def get_media_requests(self, item, info):
        img_url = item['img_urls']
        meta = {'filename': item['filename']}
        yield Request(url=img_url, meta=meta)