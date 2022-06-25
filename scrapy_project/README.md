# scrapy_project
The **scrapy project** folder contains one generic spider for **istockphoto**, **unsplash** and **shutterstock**.<br/>
It takes data from json file for the URL, query parameters and results path.<br/>
There is also a config file to get the value of which site to crawl.<br/>
It downloads images and saves metadata in csv files.<br/>
The spiders take only the **JSON response**, which contain only the data.<br/>
Images are downloaded in the **image folder**, the metadata csv files in the **csv folder**, and logs in the **logs** folder.<br/>
The csv filenames and folder filenames contain the **timestamp** of the download.<br/>

The image metadata is composed of the following:
- scraper host / site name
- search_key (eg: "people", "portrait", "face")
- filename (has the pattern: **\<website>_\<image id>**, eg: **istockphoto_123155457**)
- img_urls (the URL of the image downloaded)
- ethnicity (african/caucasian/eastasian/etc)
- description (contents of "caption", "title" or "alt" tags)
- img_type (photography/photo)
