import scrapy
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from freepik_spider.items import FreepikSpiderItem


class FreepikPhotosSpider(scrapy.Spider):
  name = 'freepik_photos'
  allowed_domains = ["freepik.com"]

# Idea:
  # The filters applied to each page (e.g gender, ethnicity, etc.) are reflected in the page url
  # Build list with the starting urls (224 starting urls in total)
  gender = ["feminine", "masculine"]
  search_keyword = ["people", "portrait", "face", "person"]
  nr_of_people = ["1", "2", "3", "4"]  
  ethnicity = ["white","hispanic", "indian", "southasian", "middleeastern", "eastasian", "black"]
  urls=[]
  for i in search_keyword:
    for g in gender:
      for j in ethnicity:
        for k in nr_of_people:    
          url = ["https://freepik.com/search?demographic=number{}%2C{}%2C{}&format=search&people=include&query={}&type=photo".format(k,g,j,i)]
          urls.append(url)  
  # Flattening the nested list so it can be read by start_urls          
  def flatten(l):
    return [item for sublist in l for item in sublist]
  urls_flat = flatten(urls)
  # Start_urls require "," to be the last element of the list
  urls_flat.append(",")

  start_urls = urls_flat  

  # Saving the scrapped data in a CSV file   
  custom_settings = {"FEEDS":{"Scraped_data.csv":{"format":"csv"}}} 


# Idea: 
  # Step 1: Collect the urls of all images on the first page (these urls lead to a new page for each image, where details of the image can be found e.g. description, tags, size)
  # Step 2: Collect the url for the "next page" and create full accessible link from it
  # Step 3: For each page in Step 2, iterate through the links collected in Step 1 and parse the needed image details (e.g. image tags, image description, image size, etc.)  

  def parse(self, response):
    photos = response.xpath('//*[@class="showcase__link"]/@href').extract()
    for photo in photos:
      absolute_url = response.urljoin(photo)
      filters = response.xpath('//*[@class="button--xs"]/text()').extract()

      # Passsing the filters information from the parse function to the parse_photo function (using meta)
      yield Request(absolute_url, callback=self.parse_photo,meta={'filters':filters})

    # Processing next page
    partial_next_page_url = response.xpath('//*[@class="pagination__next button floatl pd-y-none-i"]/@href').extract_first()
    full_next_page_url = response.urljoin(partial_next_page_url)
    
    yield Request(full_next_page_url,callback=self.parse)

  # Populating the item fields with the parsed data
  def parse_photo(self, response):
    itlo = ItemLoader(item=FreepikSpiderItem(), response=response)
    
    filters = response.meta['filters']

    image_description = response.xpath('//h1/text()').extract_first()
    image_tags = response.xpath('//*[@class="search__link"]/text()').extract()
    image_main_keywords = response.xpath('//*[@id="main"]/section/@data-main-keywords').extract()
    image_main_keywords_sponsor = response.xpath('//*[@id="main"]/section/@data-main-keywords-sponsor').extract()
    image_id = response.xpath('//*[@id="main"]/section/@data-id').extract() 
    image_width = response.xpath('//*[@id="main"]/section/@data-w').extract()
    image_height = response.xpath('//*[@id="main"]/section/@data-h').extract()
    image_urls = response.xpath('//*[@class="detail__gallery--content "]/img/@src').extract_first()
  
    itlo.add_value('image_description', image_description)
    itlo.add_value('image_tags', image_tags)
    itlo.add_value('image_main_keywords', image_main_keywords)
    itlo.add_value('image_main_keywords_sponsor', image_main_keywords_sponsor)
    itlo.add_value('image_id', image_id)
    itlo.add_value('image_width', image_width)
    itlo.add_value('image_height', image_height)
    itlo.add_value('image_urls', image_urls)
    itlo.add_value('filters', filters)

    return itlo.load_item()


