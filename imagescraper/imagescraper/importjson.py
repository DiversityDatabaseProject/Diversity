# CREATED BY NATHALIE DESCUSSE-BROWN AND UPDATED 16/01/21
# THIS FILE DOWNLOADS LIST OF FILES THAT WERE PREVIOUSLY SCRAPED WITH SCRAPY
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
from os import listdir
from os.path import isfile, join

mypath='C:/Users/natha/DSTI/Project/Diversity/unsplash-crawler/imagescraper/shutterstock_images_photosofpeoplefaces/files'

with open("C:/Users/natha/DSTI/Project/Diversity/unsplash-crawler/imagescraper/shutterstocksurls_downloaded.csv", "a", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(type(onlyfiles[3]))
    for myphoto in onlyfiles:
        writer.writerow([myphoto])