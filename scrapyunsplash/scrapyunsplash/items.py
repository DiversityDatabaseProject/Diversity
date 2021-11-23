# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy.item import Item

class ImgData(Item):
    image_urls=scrapy.Field()
