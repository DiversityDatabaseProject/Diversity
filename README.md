# scrapy_project
The **scrapy project** folder contains spiders for **istockphoto**, **unsplash** and **shutterstock**.<br/>
It downloads images and saves metadata in csv files.<br/>
The spiders take only the **JSON response**, which contain only the data.<br/>
Images are downloaded in the image folder, and the metadata csv files in the csv folder.<br/>
The csv filenames and folder filenames contain the **timestamp** of the download.<br/>
There is also logging for **istockphoto** spider.<br/>

The image metadata is composed of the following:
- scraper host / site name
- search_key (eg: "people", "portrait", "face")
- filename (has the pattern: **\<website>_\<image id>**, eg: **istockphoto_123155457**)
- img_urls (the URL of the image downloaded)
- ethnicity (african/caucasian/eastasian/etc)
- description (contents of "caption", "title" or "alt" tags)
- img_type (photography/photo)
