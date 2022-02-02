import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
import urllib
from ..items import DiversityCrawlerItem
import json
import os, time

class UnsplashSpider(scrapy.Spider):
    name = 'unsplash'
    allowed_domains = ['unsplash.com']
    start_urls = ['http://unsplash.com/']
    site = 'unsplash'
    page_cnt=100

    custom_settings = {
        'ITEM_PIPELINES': {
            'diversity_crawler.pipelines.DataWriterPipeline': 300
        }
    }

    params = {'query': 'human faces',
			'per_page': 20,
            'page': 1,
            'xp': 'search-multi-word'
		}
    
    folder=time.strftime('%Y%m%d%H%M%S',time.localtime())
    
    start_urls = []
    #for i in range(0,params['page[size]']):
    for i in range(1,page_cnt):
        start_urls.append('https://unsplash.com/napi/search/photos?'+ urllib.parse.urlencode(params))
        params['page'] = i

    #def __init__(self):
        #os.makedirs('images/'+self.folder)

    def parse(self, response):
        response =json.loads(response.body)
        #self.page_cnt = response['meta']['pagination']['totalPages'] - 11873,
        for result in response['results']:
            item = DiversityCrawlerItem()
            item['folder'] = self.folder
            item['host'] =  self.name
            item['search_key'] =  self.params['query']
            item['ethnicity'] =  'NA'#self.params['filter[people_ethnicity]']
            item['img_urls'] =  result['urls']['small']
            item['filename'] =  self.site+'_'+result['id']
            item['description'] =  result['alt_description'].replace(',','')
            item['img_type'] =  'NA'
            if len(item['img_urls']) != 0:
                urllib.request.urlretrieve(item['img_urls'], 'images/unsplash/'+item['filename']+'.jpg')
            yield item