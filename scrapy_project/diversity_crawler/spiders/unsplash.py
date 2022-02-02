import scrapy
from scrapy.utils.log import configure_logging
import urllib
from ..items import DiversityCrawlerItem
import json
import time
import logging

class UnsplashSpider(scrapy.Spider):
    name = 'unsplash'
    allowed_domains = ['unsplash.com']
    start_urls = ['http://unsplash.com/']
    site = 'unsplash'

    custom_settings = {
        'ITEM_PIPELINES': {
            'diversity_crawler.pipelines.DataWriterPipeline': 300
        },
        'LOG_STDOUT':True
    }

    configure_logging(install_root_handler=False)

    logging.basicConfig(
        filename='logs/unsplash_log.txt',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    params = {'query': 'people',
			'per_page': 20,
            'page': 1,
            'xp': 'search-multi-word'
		}
    
    folder=time.strftime('%Y%m%d%H%M%S',time.localtime())
    start_urls = ['https://unsplash.com/napi/search/photos?'+ urllib.parse.urlencode(params)]

    def parse(self, response):
        base_url = 'https://unsplash.com/napi/search/photos?'
        data = json.loads(response.body)
        page_cnt = data['total_pages']
        print("number of pages: ", page_cnt)
        logging.info("number of pages: ", page_cnt)
        for page in range(1, page_cnt):
            self.params['page'] = page
            yield scrapy.Request(base_url + urllib.parse.urlencode(self.params), dont_filter=True, callback=self.parse_page)

    #def __init__(self):
        #os.makedirs('images/'+self.folder)

    def parse_page(self, response):
        response =json.loads(response.body)
        for result in response['results']:
            item = DiversityCrawlerItem()
            item['folder'] = self.folder
            item['host'] =  self.name
            item['search_key'] =  self.params['query']
            item['ethnicity'] =  'NA'#self.params['filter[people_ethnicity]']
            item['img_urls'] =  result['urls']['small']
            item['filename'] =  self.site+'_'+result['id']
            if result['alt_description'] is not None:
                item['description'] =  result['alt_description'].replace(',','')
            else:
                item['description'] =  'NA'
            item['img_type'] =  'NA'
            if len(item['img_urls']) != 0:
                urllib.request.urlretrieve(item['img_urls'], 'images/unsplash/'+item['filename']+'.jpg')
            yield item

    