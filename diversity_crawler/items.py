# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DiversityCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    host= scrapy.Field()
    search_key=scrapy.Field()
    img_urls = scrapy.Field()
    filename = scrapy.Field()
    description = scrapy.Field()
    img_type  = scrapy.Field()
    ethnicity  = scrapy.Field()
    folder = scrapy.Field()
    last_page = scrapy.Field()
    pass
