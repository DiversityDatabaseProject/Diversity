'''
This spider is a generic spider for istockphoto.com, unsplash.com and shutterstock.com
It takes the JSON data from utils/site_data.json file to parse the web site, query parameters and results path
It gets the environment variable, HOME_DIR as the project folder
The utils/crawler.ini contains the configuration file such as which site is going to be scraped
It takes the JSON response from the web sites, which contain only data (no formatting), for faster download and
less burden to the web servers
Images are downloaded together with the metadata
The images are saved in the images folder, the csv in csv folder, and the log files in the logs folder
'''
import scrapy
from scrapy.utils.log import configure_logging
import logging
import urllib
from ..items import DiversityCrawlerItem
import json
import os, time
import configparser

class GenericSpiderSpider(scrapy.Spider):
    name = 'generic_spider'
    site = ''
    allowed_domains = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'diversity_crawler.pipelines.DataWriterPipeline': 300
        },
        'LOG_STDOUT':True
    }

    site_data = []
    params = []
    
    
    images_folder=''

    start_urls = []
    
    def __init__(self):
        HOME_DIR = os.getenv('CRAWLER_HOME')
        config = configparser.ConfigParser()
        config.read('utils/crawler.ini')
        
        self.site = config['APP']['SITE']
        self.allowed_domains = ['shutterstock']

        configure_logging(install_root_handler=False)

        #create images folder, if not existing
        if os.path.isdir(HOME_DIR+config['APP']['IMAGES_FOLDER']):
            pass
        else:
            os.makedirs(HOME_DIR+config['APP']['IMAGES_FOLDER'])

        timestamp = time.strftime('%Y%m%d%H%M%S',time.localtime())
        self.images_folder = HOME_DIR+config['APP']['IMAGES_FOLDER']+'/'+self.site+'_'+timestamp

        #create the folder for the images to be downloaded
        os.makedirs(self.images_folder)
        
        #create logs folder, if not existing
        if os.path.isdir(HOME_DIR+config['APP']['LOG_FOLDER']):
            pass
        else:
            os.makedirs(HOME_DIR+config['APP']['LOG_FOLDER'])
        

        logging.basicConfig(
            filename=HOME_DIR+config['APP']['LOG_FOLDER']+'/'+self.site+'_log.txt',
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        with open("utils/site_data.json", encoding='utf-8', errors='ignore') as json_data:
            json_data = json.load(json_data, strict=False)
        for item in json_data:
            print(item.get('site'))
            if item.get('site')==self.site:
                print("ano ba to: ",item['start_urls'])
                self.start_urls.append(item['start_urls'] + urllib.parse.urlencode(item['params']))
                self.params = item['params']
                self.site_data = item
                print("SITE DATA: ", self.site_data)

    def parse(self, response):
        base_url = self.site_data['start_urls']
        data = json.loads(response.body)
        page_cnt=1
        
        if self.site == 'unsplash':
            page_cnt =  data[self.site_data['page_cnt']]  
        else:
            page_cnt =  data[self.site_data['page_cnt_1']][self.site_data['page_cnt_2']][self.site_data['page_cnt_3']]

        print("number of pages: ", page_cnt)
        logging.info("number of pages: ", page_cnt)
        for page in range(1, page_cnt):
            self.params[self.site_data['params_key']['page']] = page
            yield scrapy.Request(base_url + urllib.parse.urlencode(self.params), dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        response =json.loads(response.body)
        data = ''
        if self.site=='istockphoto':
            data = response[self.site_data['result_1']][self.site_data['result_2']]
        else:
            data = response[self.site_data['result']]
        for result in data:
            img_url = ''
            if self.site == 'istockphoto':
                img_url = result[self.site_data['results']['img_urls']]
            else:
                img_url = result[self.site_data['results']['img_urls_1']][self.site_data['results']['img_urls_2']]
                
            #img_url = result['urls']['small']
            if img_url is not None:
                item = DiversityCrawlerItem()
                item['folder'] = self.folder
                item['host'] =  self.name
                #print("self.site_data['params_key']['search_key']: ", self.site_data['params_key']['search_key'])
                item['search_key'] =  self.params[self.site_data['params_key']['search_key']]
                item['ethnicity'] =  'NA'
                if self.site != "unsplash":
                    item['ethnicity'] =  self.params[self.site_data['params_key']['ethnicity']]
                item['img_urls'] =  img_url
                item['filename'] =  self.site+'_'+result[self.site_data['results']['filename']]
                item['description'] = 'NA'
                if self.site =='shutterstock':
                    item['description'] =  result[self.site_data['results']['description_1']][self.site_data['results']['description_2']].replace(',','')
                else:
                    item['description'] =  result[self.site_data['results']['description']].replace(',','')
                item['img_type'] =  'NA'
                if self.site == 'shutterstock':
                    item['img_type'] =  result[self.site_data['results']['img_type_1']][self.site_data['results']['img_type_2']]
                else:
                    item['img_type'] =  result[self.site_data['results']][self.site_data['img_type']]
                urllib.request.urlretrieve(item['img_urls'], self.images_folder+'/'+item['filename']+'.jpg')
                yield item
