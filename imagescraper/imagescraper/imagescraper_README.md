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
is the defautl scrapy project structure and is automatically created when
creating a scraoy object.

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
