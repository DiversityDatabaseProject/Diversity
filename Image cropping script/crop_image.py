from PIL import Image
import glob
import os
paths = {
    'IMAGE_TOCROP_PATH': os.path.join('crop-images', 'pre-process'), 
    'CROPPED_PATH': os.path.join('crop-images', 'post-process'), 
 }

#creating our folders 
for path in paths.values():
    if not os.path.exists(path):
            !mkdir {path}
            
#create a list of the images to crop
image_list = [i for i in glob.glob(os.path.join('crop-images', 'pre-process','*jpg'))]

# resized/cropped images to list
for i in image_list:
    '''
    Crop the bottom 20 pixels for the images. 
    Images will be overriden
    '''
    cropped_images = Image.open(i)
    cropped_images = cropped_images.crop((0, 0, cropped_images.width, cropped_images.height - 20))
    cropped_images.save(i)



    


   
