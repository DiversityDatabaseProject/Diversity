import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
import urllib
from ..items import DiversityCrawlerItem
import json
import os, time


class ShutterstockSpider(scrapy.Spider):
    name = 'shutterstock'
    allowed_domains = ['shutterstock.com']
    site = 'shutterstock'
    page_cnt=3

    params = {'language': 'en',
			'namespace': 'shutterstock',
			'page[number]': 1,
			'page[size]': 100,
			'q': 'people',
			'queryTranslations': 'true',
			'filter[people_ethnicity]': 'african',
			'filter[image_type]': 'photo',
			'filter[is_model_released]': 'true'
		}
    
    folder=time.strftime('%Y%m%d%H%M%S',time.localtime())
    
    start_urls = []
    for i in range(0,params['page[size]']):
        start_urls.append('https://www.shutterstock.com/napi/images/search?'+ urllib.parse.urlencode(params))
        params['page[number]'] += 1

    def __init__(self):
        os.makedirs('images/'+self.folder)

    def parse(self, response):
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
