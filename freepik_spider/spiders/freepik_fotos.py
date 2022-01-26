import scrapy
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from freepik_spider.items import FreepikSpiderItem

class FreepikFotosSpider(scrapy.Spider):
    name = 'freepik_fotos'
    allowed_domains = ["freepik.com"]
    start_urls = ['https://www.freepik.com/search?format=search&query=black%20apple%20gold&selection=1&type=photo']
    # This is a test url - To be updated at the end! 
    #'https://www.freepik.com/search?format=search&query=portrait%20face&type=photo'

    # Idea: 
    # Step 1: Collect the urls of all images on the first page (these urls lead to a new page for each image, where e.g. description and tags can be found)
    # Step 2: Collect the url for the "next page" and create full link out of it
    # Step 3: Iterate through all the pages while collecting data as is step 1 and step 2 
    # Step 3: Go to the url of each image from step 1 and extract: title, tags and link to the original image that will be downloaded


    def parse(self, response):
        fotos = response.xpath('//*[@class="showcase__link"]/@href').extract()
        
        for foto in fotos:
            absolute_url = response.urljoin(foto)
            yield Request(absolute_url, callback=self.parse_foto)

        # Process next page
        partial_next_page_url = response.xpath('//*[@class="pagination__next button floatl pd-y-none-i"]/@href').extract_first()
        full_next_page_url = response.urljoin(partial_next_page_url)
        yield Request(full_next_page_url)

    def parse_foto(self, response):
        l = ItemLoader(item=FreepikSpiderItem(), response=response)

        image_title = response.xpath('//h1/text()').extract_first()
        image_tags = response.xpath('//*[@class="search__link"]/text()').extract()
    
        image_urls = response.xpath('//*[@class="detail__gallery--content "]/img/@src').extract_first()

        l.add_value('image_title', image_title)
        l.add_value('image_tags', image_tags)
        l.add_value('image_urls', image_urls)

        return l.load_item()