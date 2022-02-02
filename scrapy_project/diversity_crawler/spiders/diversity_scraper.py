import scrapy
from scrapy.utils.log import configure_logging
import logging
import urllib
from ..items import DiversityCrawlerItem
import json
import os, time

class DiversityScraperSpider(scrapy.Spider):
    name = 'diversity_scraper'
    allowed_domains = ['istockphoto.com']
    site = 'istockphoto'
    page_cnt=100

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT ': 2,
        'ITEM_PIPELINES': {
            'diversity_crawler.pipelines.DataWriterPipeline': 300
        },
        'LOG_STDOUT':True
    }

    folder=time.strftime('%Y%m%d%H%M%S',time.localtime())
    configure_logging(install_root_handler=False)

    logging.basicConfig(
        filename='logs/'+folder+'_log.txt',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    params = {
            'ethnicity': 'nativeamericanfirstnations',
            'page': 1,
            'phrase': 'portrait'
    }
    
    start_urls = ['https://www.istockphoto.com/en/search/2/image?'+ urllib.parse.urlencode(params)]

    def __init__(self):
        os.makedirs('images/'+self.folder)

    def parse(self, response):
        base_url = 'https://www.istockphoto.com/en/search/2/image?'
        data = json.loads(response.body)
        page_cnt = data['gallery']['lastPage']
        print("number of pages: ", page_cnt)
        logging.info("number of pages: ", page_cnt)
        for page in range(1, page_cnt):
            self.params['page'] = page
            yield scrapy.Request(base_url + urllib.parse.urlencode(self.params), dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        response =json.loads(response.body)
        for result in response['gallery']['assets']:
            item = DiversityCrawlerItem()
            item['folder'] = self.folder
            item['host'] =  self.name
            item['search_key'] =  self.params['phrase'] +' '+ self.params['ageofpeople']
            item['ethnicity'] =  self.params['ethnicity']
            item['img_urls'] =  result['thumbUrl']
            item['filename'] =  self.site+'_'+result['id']
            item['description'] =  result['altText'].replace(',','')
            item['img_type'] =  result['mediaType']
            item['last_page'] = self.params['page']
            if len(result['thumbUrl']) != 0:
                urllib.request.urlretrieve(result['thumbUrl'], 'images/'+self.folder+'/'+item['filename']+'.jpg')
            yield item
