import scrapy
import urllib3
from imagescraper.items import ImgData

class ImagescraperSpider(scrapy.Spider):
    name = "imagescraper"
    start_urls = [
              'https://www.shutterstock.com/search/photos+of+people+faces'
              #'https://www.istockphoto.com/en/search/2/image?phrase=photos%20of%20people&family=creative'
              #'https://www.pinterest.co.uk/search/pins/?q=photos%20of%20people&rs=typed&term_meta[]=photos%7Ctyped&term_meta[]=of%7Ctyped&term_meta[]=people%7Ctyped'
        ]

    def parse(self, response):
        images = ImgData()
        images['image_urls']=[] 
        for imagescraper in response.css('img::attr(src)'):
            if response.css('img::attr(alt)') !='istock logo':
                pass
            else :
             images['image_urls'].append(imagescraper.get())

        yield images

       
