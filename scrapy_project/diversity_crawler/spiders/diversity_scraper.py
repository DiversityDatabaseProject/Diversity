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
            'phrase': 'people',
            'ageofpeople':'teenager'
    }
    
    start_urls = []
    istockphoto_url = 'https://www.istockphoto.com/en/search/2/image?'
    
    for i in range(0,page_cnt):
        #start_urls.append('http://api.scraperapi.com?api_key=844b745e48cac6f2abae870dbd3a4f92&url=' + istockphoto_url + urllib.parse.urlencode(params) + '&keep_headers=true')
        start_urls.append('https://www.istockphoto.com/en/search/2/image?' + urllib.parse.urlencode(params))
        params['page'] += 1

    def __init__(self):
        os.makedirs('images/'+self.folder)

    def parse(self, response):
        response =json.loads(response.body)
        self.page_cnt=response['gallery']['lastPage']
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
