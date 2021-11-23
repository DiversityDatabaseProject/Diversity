import scrapy
import urllib3
from scrapyunsplash.items import ImgData

class QuotesSpider(scrapy.Spider):
    name = "scrapyunsplash"
    start_urls = [
              'https://unsplash.com/s/photos/portraits'
        ]

    def parse(self, response):
        images = ImgData()
        images['image_urls']=[] 
        for scrapyunsplash_images in response.css('img::attr(src)'):
            images['image_urls'].append(scrapyunsplash_images.get())

        yield images

       
