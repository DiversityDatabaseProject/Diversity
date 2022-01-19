from PIL import Image
import glob


#create a list of the images to crop
image_list = [i for i in glob.glob('YOUR_DIRECTORY\\*.jpg')]

# resized/cropped images to list
for i in image_list:
    '''
    Crop the bottom 15 pixels for the images. 
    Images will be overriden
    '''
    cropped_images = Image.open(i)
    cropped_images = cropped_images.crop((0, 0, cropped_images.width, cropped_images.height - 20))
    cropped_images.save(i)




    


   