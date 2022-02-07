# IMAGE SCRAPER CREATED BY NATHALIE DESCUSSE-BROWN AND UPDATED 16/01/21
# TWO SPIDERS: SPD1 SCRAPES PHOTOS FROM WEBSITE SHUTTERSTOCK AND SAVES THEM LOCALLY
# SP2 STORES URL AND DESCRIPTION IN SEPARATE CSV FILE 
# ONE KNOWN ISSUE IS THAT SPD2 MAY NOT LIST SAME FILES AS IMAGES DOWNLOADED BY SPD1 AS 
# WEBSITE DOESN'T APPEAR TO HAVE A SET ORDER FOR PICTURES. SO IF RUNNING BOTH, ENSURE ALL
# PICTURES FOR SPECIFIC SEARCH ARE RETURNED.
import scrapy
import urllib3
from imagescraper.items import Myspd2spiderItem
from imagescraper.items import Myspd1spiderItem
from scrapy.crawler import CrawlerProcess
from scrapy import Selector
import json
from bs4 import BeautifulSoup
import sys

#THE BELOW DEFINES SPIDER SPD1 INCLUDING ITS NAME THAT NEEDS TO BE CALLED TO RUN THE SPIDER
# START_URLS INDICATES SITE TO BE SCRAPED
class Myspd1Spider(scrapy.Spider):
    name = "myspd1"
    #custom_settings = {"FEEDS" : {"imagescraper_shutterstock.csv":{"format":"csv"}}}

    start_urls = ["https://www.shutterstock.com/search/photos+of+people+faces"]
    #start_urls = ["https://www.shutterstock.com/_next/data/Ma8REdqbRY1obIg3sjxO2/en/_shutterstock/search/photos%2Bof%2Bpeople%2Bfaces.json?term=photos%2Bof%2Bpeople%2Bfaces"]

    base_url='https://www.shutterstock.com/'
    custom_settings = {
        'ITEM_PIPELINES': {'imagescraper.pipelines.Myspd1spiderPipeline': 300},
    }
    i=2
    print('type_start_url',type(start_urls[0]))

#THE PARSE FUNCTION BELOW IS REQUIRED TO EXTRACT THE INDIVIDUAL IMAGE URLS FROM THE WEBSITE JSON FILE
#THE FUNCTION THEN SAVES THE SCRAPY ITEM THAT WILL BE SUBSEQUENTLY BE PROCESSED BY THE PIPELINE.PY SCRIPT,
#ENABLING IT TO SAVE TO LOCAL FOLDER

    def parse(self, response):
        images = Myspd1spiderItem()
        images['image_urls']=[] 

        soup= BeautifulSoup(response.text,'html.parser')
        script = soup.find_all('script')[4].text.strip()[0:]
        jsonlist = []

        concatjson = '{"foo":' + script + "}"
        data = json.loads(concatjson)
        for imagescraper in data["foo"]:
              images['image_urls'].append(imagescraper["url"])

        yield images
    
    # THE CODE BELOW IS REQUIRED TO HANDLE PAGINATION THROUGHOUT THE WEBSITE
        next_page_url = str(self.base_url) + '/search/photos+of+people+faces?page=' + str(self.i)
        print(self.i,'next_page_url',type(next_page_url))
        yield scrapy.Request(str(next_page_url), callback=self.parse) 
        if self.i<4981 :
            self.i=self.i+1;  
        else:
            pass


#THE BELOW DEFINES SPIDER SPD2 INCLUDING ITS NAME THAT NEEDS TO BE CALLED TO RUN THE SPIDER
#START_URLS INDICATES SITE TO BE SCRAPED
#CSV FILE WHERE DATA SCRAPED WILL BE STORED IS ALSO SPECIFIED
class Myspd2Spider(scrapy.Spider):
    name = "myspd2"
    custom_settings = {
        'ITEM_PIPELINES': {'imagescraper.pipelines.Myspd2spiderPipeline': 300},
        "FEEDS" : {"imagescraper_shutterstock.csv":{"format":"csv"}},
    }

    start_urls = ["https://www.shutterstock.com/search/photos+of+people+faces"]

    base_url='https://www.shutterstock.com/'
    i=2
    
#THE PARSE FUNCTION BELOW IS REQUIRED TO EXTRACT THE INDIVIDUAL IMAGE URLS FROM THE WEBSITE JSON FILE
#THE FUNCTION THEN SAVES THE SCRAPY ITEM THAT WILL BE SUBSEQUENTLY BE PROCESSED BY THE PIPELINE.PY SCRIPT,
#ENABLING IT TO SAVE BOTH URL AND DESCRIPTION TO A CSV FILE

    def parse(self, response):
        images = Myspd2spiderItem()
        images['image_urls']=[] 
        images['image_description']=[] 


        soup= BeautifulSoup(response.text,'html.parser')
        script = soup.find_all('script')[4].text.strip()[0:]
        jsonlist = []

        concatjson = '{"foo":' + script + "}"
        data = json.loads(concatjson)
        for imagescraper in data["foo"]:
              images['image_urls'].append(imagescraper["url"])
              images['image_description'].append(imagescraper["description"])

        yield images

  
        # THE CODE BELOW IS REQUIRED TO HANDLE PAGINATION THROUGHOUT THE WEBSITE
        next_page_url = str(self.base_url) + '/search/photos+of+people+faces?page=' + str(self.i)
        print(self.i,'next_page_url',type(next_page_url))
        yield scrapy.Request(str(next_page_url), callback=self.parse) 
        if self.i<4981 :
            self.i=self.i+1;  
        else:
            pass
