import scrapy
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from freepik_spider.items import FreepikSpiderItem

class FreepikFotosSpider(scrapy.Spider):
    name = 'freepik_fotos'
    allowed_domains = ["freepik.com"]
    start_urls = ["https://www.freepik.com/search?demographic=number1%2Chispanic&format=search&people=include&query=portrait&type=photo"]
  # search keyword: "portrait" /1 person/ 7 ethnicities
    # ["https://www.freepik.com/search?demographic=number1%2Chispanic&format=search&people=include&query=portrait&type=photo"]
    # ["https://www.freepik.com/search?demographic=number1%2Csouthasian&format=search&people=include&query=portrait&type=photo"]
    # ['https://www.freepik.com/search?demographic=number1%2Cmiddleeastern&format=search&people=include&query=portrait&type=photo']
    # ['https://www.freepik.com/search?demographic=number1%2Ceastasian&format=search&people=include&query=portrait&type=photo']
    # ['https://www.freepik.com/search?demographic=number1%2Cwhite&format=search&people=include&query=portrait&type=photo']
    # ["https://www.freepik.com/search?demographic=number1%2Cblack&format=search&people=include&query=portrait&type=photo"]
    # ['https://www.freepik.com/search?demographic=number1%2Cindian&format=search&people=include&query=portrait&type=photo']
  # search keyword: "face" /1 person/ 7 ethnicities
    # ["https://www.freepik.com/search?demographic=number1%2Cwhite&format=search&people=include&query=face&type=photo"]
    # ["https://www.freepik.com/search?demographic=number1%2Cindian&format=search&people=include&query=face&type=photo"]
    # ["https://www.freepik.com/search?demographic=number1%2Chispanic&format=search&people=include&query=face&type=photo"]
    # ["https://www.freepik.com/search?demographic=number1%2Ceastasian&format=search&people=include&query=face&type=photo"]
    # ["https://www.freepik.com/search?demographic=number1%2Cmiddleeastern&format=search&people=include&query=face&type=photo"]
    # ["https://www.freepik.com/search?demographic=number1%2Csouthasian&format=search&people=include&query=face&type=photo"]
    # ["https://www.freepik.com/search?demographic=number1%2Cblack&format=search&people=include&query=face&type=photo"]

    # Name of the file to be updated    
    custom_settings = {"FEEDS":{"Portrait_hispanic_1person.csv":{"format":"csv"}}} 

    # Idea: 
    # Step 1: Collect the urls of all images on the first page (these urls lead to a new page for each image, where e.g. description and tags can be found)
    # Step 2: Collect the url for the "next page" and create full link out of it
    # Step 3: Iterate through all the pages while collecting data as in step 1 and step 2 
    # Step 3: Go to the url of each image from step 1 and extract: link to the original image that will be downloaded as well as other data such as image title, tags, size, etc.


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
        itlo = ItemLoader(item=FreepikSpiderItem(), response=response)

        image_description = response.xpath('//h1/text()').extract_first()
        image_tags = response.xpath('//*[@class="search__link"]/text()').extract()
        image_main_keywords = response.xpath('//*[@id="main"]/section/@data-main-keywords').extract()
        image_main_keywords_sponsor = response.xpath('//*[@id="main"]/section/@data-main-keywords-sponsor').extract()
        image_id = response.xpath('//*[@id="main"]/section/@data-id').extract() 
        image_width = response.xpath('//*[@id="main"]/section/@data-w').extract()
        image_height = response.xpath('//*[@id="main"]/section/@data-h').extract()

        image_urls = response.xpath('//*[@class="detail__gallery--content "]/img/@src').extract_first()
        # this link leads to the full image, big size
        # to download the small images: image_urls = response.xpath('//*[@id="main"]/section/@data-image-small').extract_first()
        # to download the mini images: image_urls = response.xpath('//*[@id="main"]/section/@data-image-mini').extract_first()

        itlo.add_value('image_description', image_description)
        itlo.add_value('image_tags', image_tags)
        itlo.add_value('image_main_keywords', image_main_keywords)
        itlo.add_value('image_main_keywords_sponsor', image_main_keywords_sponsor)
        itlo.add_value('image_id', image_id)
        itlo.add_value('image_width', image_width)
        itlo.add_value('image_height', image_height)
        itlo.add_value('image_urls', image_urls)

        return itlo.load_item()
