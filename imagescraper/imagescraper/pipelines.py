# THIS CODE CREATES TWO SEPARATE PIPELINES FOR TWO SPIDERS SPD1 AND SPD2
# THE FIRST PIPELINE SAVES IMAGES TO LOCAL FOLDER
# THE SECOND PIPELINE SAVES IMAGES URL AND DESCRIPTION TO CSV FILE LOCALLY
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# CREATED BY NATHALIE DESCUSSE-BROWN AND UPDATED 16/01/21

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from urllib.parse import urlparse


from scrapy.pipelines.images import ImagesPipeline

#THE BELOW PIPELINE Myspd1spiderPipeline WAS CREATED FOR SPIDER SPD1 TO SAVE IMAGES IN LOCAL FOLDER 'files' 
#AND MODIFY IMAGE FILENAME TO INCLUDE URL
class Myspd1spiderPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        return 'files/' + os.path.basename(urlparse(request.url).path)

#THE BELOW PIPELINE Myspd2spiderPipeline WAS CREATED FOR SPIDER SPD1 TO SAVE URL AND
#IMAGE DESCRIPTION IN A CSV FILE LOCALLY
class Myspd2spiderPipeline(object):
    def process_item(self,item,spider):
        return item

