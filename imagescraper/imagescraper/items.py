# THIS CODE DEFINES THE MODEL FOR TWO SPIDER OBJECTS
# FOR SPIDERS SPD1, THAT SAVES IMAGES LOCALLY
# AND FOR SPD2 THAT SAVES URL AND IMAGE DESCRIPTION
# IN A LOCAL CSV FILE
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# CREATED BY NATHALIE DESCUSSE-BROWN AND UPDATED 16/01/21

import scrapy
from scrapy.item import Item

class MymultispiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Myspd1spiderItem(Item):
    image_urls=scrapy.Field()

class Myspd2spiderItem(Item):
    image_urls=scrapy.Field()
    images=scrapy.Field()
    image_description=scrapy.Field()

