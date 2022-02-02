import scrapy
from scrapy.utils.log import configure_logging
import urllib
from ..items import DiversityCrawlerItem
import json
import os, time
import logging

class ShutterstockSpider(scrapy.Spider):
    name = 'shutterstock'
    allowed_domains = ['shutterstock.com']
    site = 'shutterstock'
    page_cnt=500

    configure_logging(install_root_handler=False)

    logging.basicConfig(
        filename='logs/unsplash_log.txt',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    params = {'language': 'en',
			'namespace': 'shutterstock',
			'page[number]': 6,
			'page[size]': 100,
			'q': 'people',
			'queryTranslations': 'true',
			'filter[people_ethnicity]': 'east_asian',
			'filter[image_type]': 'photo',
			'filter[is_model_released]': 'true',
            'sort': 'newest'
		}
    
    folder=time.strftime('%Y%m%d%H%M%S',time.localtime())
    
    def __init__(self):
        os.makedirs('images/'+self.folder)

    start_urls = ['https://www.shutterstock.com/napi/images/search?'+ urllib.parse.urlencode(params)]

    def parse(self, response):
        base_url = 'https://www.shutterstock.com/napi/images/search?'
        data = json.loads(response.body)
        page_cnt = data['meta']['pagination']['totalPages']
        print("number of pages: ", page_cnt)
        logging.info("number of pages: ", page_cnt)
        for page in range(1, page_cnt):
            self.params['page[number]'] = page
            yield scrapy.Request(base_url + urllib.parse.urlencode(self.params), dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        response =json.loads(response.body)
        for result in response['data']:
            item = DiversityCrawlerItem()
            item['folder'] = self.folder
            item['host'] =  self.name
            item['search_key'] =  self.params['q']
            item['ethnicity'] =  self.params['filter[people_ethnicity]']
            item['img_urls'] =  result['attributes']['src']
            item['filename'] =  self.folder+'/'+self.site+'_'+result['id']+'.jpg'
            item['description'] =  result['attributes']['alt'].replace(',','')
            item['img_type'] =  result['attributes']['imageType']
            yield item
