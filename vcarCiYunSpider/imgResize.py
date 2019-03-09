
from PIL import Image

class ImgReSize(object):
    im = Image.open("/Users/guohan/Desktop/sc.png")
    im_resized = im.resize((128, 128))
    # im_resized.show()
    im_resized.save('/Users/guohan/Desktop/sc3.png')



imgReSize=ImgReSize()