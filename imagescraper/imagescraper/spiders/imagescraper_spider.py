import scrapy
import urllib3
from imagescraper.items import ImgData

#The below defines the name of the spider and which websites will be scraped.
class ImagescraperSpider(scrapy.Spider):
    name = "imagescraper"
    start_urls = [
              'https://www.shutterstock.com/search/photos+of+people+faces'
              #'https://www.istockphoto.com/en/search/2/image?phrase=photos%20of%20people&family=creative'
              #'https://www.pinterest.co.uk/search/pins/?q=photos%20of%20people&rs=typed&term_meta[]=photos%7Ctyped&term_meta[]=of%7Ctyped&term_meta[]=people%7Ctyped'
              #'https://www.rungineer.com/blog-1/2021/5/24/jurassic-coast-half-challenge-or-the-race-that-nearly-killed-my-love-of-hills'
        ]
    base_url='https://www.shutterstock.com/'

#With the below we scrape and save the image urls scraped into the images list, that will then be saved into a local folder

    def parse(self, response):
        images = ImgData()
        images['image_urls']=[] 
        for imagescraper in response.css('img::attr(src)'):
            images['image_urls'].append(imagescraper.get())
        yield images

        # added below to navigate to following pages and scrape them also
        next_page_partial_url = response.xpath('//div[@class="z_b_f3102"]/a/@href').extract_first()
        next_page_url = self.base_url + str(next_page_partial_url)
        yield scrapy.Request(next_page_url, callback=self.parse)       
