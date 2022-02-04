---
title: "imagescraper_README"
author: "Nathalie Descusse-Brown"
date: "1/17/2022"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## Structure of imagescraper folder

The imagescraper code was created using Python scrapy library. It runs with
several linked .py scripts.

There are three levels to the imagescraper project folders, this structure
is the default scrapy project structure and is automatically created when
creating a scrapy object.

The top level is the imagescraper folder, which is just the project folder.

Underneath there is another imagecraper folder that contains most of the .py 
files required to run the spider, namely:
- items.py, where the scrapy objects are defined
- settings.py, which enables running of proxy rotation, running of pipelines,
it is in essence the enabler for the other pieces of code
- pipelines.py, which defines the pipelines for exporting of spider output


A separate file in that foler is proxy-text.py. This was created separately from
the scrapy project but is required to be run FIRST (before running the scrapy 
spider) to enabling using only valid proxies for the proxy rotation. Running 
this code checks for valid proxies and saves these proxies to a proxy-list2.txt
file which is subsequently used when running the scrapy spider.

Finally the third level down the imagescraper director is the spiders folder
that contains the spider code imagescraper_spider.py.

## How to run imagescraper spider

To run the spiders, you will need to type 'scrapy crawl spd1' in cmd line to
run the first spider (that downloads images), and 'scrapy crawl spd2' to 
run the second spider (that saves urls and description to csv file)


## URLlist csv file and associated images

It was noticed after both spiders had been run (spd1 and spd2) that for some 
reason not all downloaded images had a corresponding record in the csv file 
and vice-versa. Most likely explanation for this is that not all photos
returned by search had been scraped and similarly not all photo urls were
returned by the second spider. Assumption is that some website pages were
missing from the results and order of photos scraped by spd1 was different
than urls scraped by spd2. This remains to be investigated, although not 
critical to the final product delivered as per below.

## Metadata for the downloaded images

It was decided by the project team to retrieve metadata to enable labelling
of the pictures for modelling. Unfortunately it was noticed that since
scraping the initial ~64,000 photos Shutterstock had changed their json file and
spider in this folder is no longer working. However it was still possible to
retrieve metadata separately for the ~64,000 photos downloaded by retrieving
the metadata from the json file associated with each picture. This was enabled 
by first retrieving the urls of the photos actually downloaded - this is done with script 'importjson.py' (hence no longer relying on the csv file produced by spd2) and then scraping metadata from json with the script 'metadatagetter.py'. The metadata
is then saved in csv file 'metadata_shutterstock_downloaded.csv'

## Cropping and renaming of images

Images downloaded contained a caption with 'Shutterstock' name and ID that
needed to be removed. PIL package was used to do so, and script also renames
pictures to agreed standard name of 'shuttertstock_id'.






