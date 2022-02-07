# CREATED BY NATHALIE DESCUSSE-BROWN AND UPDATED 16/01/21
# THIS FILE DOWNLOADS METADATA FOR ALL PHOTOS LISTED IN THE SHUTTERSTOCKURLS_DOWNLOADED CSV FILE
# BEWARE OF ISSUE WITH URLOPEN OPENING CONNECTIONS BUT NO SOLUTION FOUND FOR CLOSING THEM SO MAY CRASH VSD
import csv
from csv import reader,writer
import pandas as pd
import urllib.request
import json
from bs4 import BeautifulSoup
import string
import requests
from urllib.request import urlopen


data = []
exclusions=[]

with open("C:/Users/natha/DSTI/Project/Diversity/unsplash-crawler/imagescraper/shutterstocksurls_downloaded.csv", "r", encoding="utf-8") as f:
    with open('metadata_shutterstock_downloaded.csv', 'a', newline='',encoding="utf-8") as csvfile:
        metawriter = csv.writer(csvfile)
        csv_reader = reader(f)
        # Iterate over each row in the csv using reader object
        for urlshutter in csv_reader:
            imagecategories=[]
            imagesamemodel=[]
            imagevisuallysimilar=[]
            imagesincollections=[]
            dash = urlshutter[0].rfind('-')
            imid=urlshutter[0][dash+1:-4]
            url1='https://www.shutterstock.com/napi/images/'+str(imid)+'?recordActivity=false&include=categories,contributor.categories,contained-in-collections.categories,same-model.categories,visually-similar.categories,visually-similar-videos.categories,image-scores,contributor-settings&page[contained-in-collections][size]=1&page[contained-in-collections-items][size]=20&page[visually-similar][size]=37&page[visually-similar-videos][size]=12&page[same-model][offset]=0&page[visually-similar-videos][offset]=0&page[visually-similar][offset]=7&language=en'
            try:    
                html = urlopen(url1).read()
                soup = BeautifulSoup(html, features="html.parser")
                jsonraw=soup.get_text()
                jsonsoup=json.loads(jsonraw)

                imageid=jsonsoup['data']['id']
                imagedescr=jsonsoup['data']['attributes']['alt']
                imagetags=jsonsoup['data']['attributes']['keywords']
                imagetype=jsonsoup['data']['attributes']['imageType']
                if 'smallJpg' in jsonsoup['data']['attributes']['sizes']:
                    imagedpi=jsonsoup['data']['attributes']['sizes']['smallJpg']['dpi']
                else:
                    imagedpi=''
                imagewidth=jsonsoup['data']['attributes']['width']
                imageheight=jsonsoup['data']['attributes']['height']
                try:
                    for imagescraper_samemodel in jsonsoup['data']['relationships']['sameModel']['data']:
                        imagesamemodel.append(imagescraper_samemodel['id'])
                except:
                        imagesamemodel=''
                for imagescraper_similar in jsonsoup['data']['relationships']['visuallySimilar']['data']:
                    imagevisuallysimilar.append(imagescraper_similar['id'])
                for imagescraper_categories in jsonsoup['data']['relationships']['categories']['data']:
                    imagecategories.append(imagescraper_categories['id'])
                for imagescraper_incollections in jsonsoup['data']['relationships']['containedInCollections']['data']:
                    imagesincollections.append(imagescraper_incollections['id'])
                
                metawriter.writerow([imageid, imagedescr, imagetags, imagetype, imagedpi, imagewidth, imageheight, imagesamemodel, imagevisuallysimilar, imagecategories,imagesincollections])
            except:
                exclusions.append(url1)

with open('exclusions.csv', 'a', newline='',encoding="utf-8") as exfile:
    metawriter = csv.writer(exfile)
    for exclusion in exclusions:
        metawriter.writerow([exclusion]) 

