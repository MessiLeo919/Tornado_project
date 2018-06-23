import os
import glob

from PIL import Image


def get_images(path):
    '''
    获取路径下的所有JPG图片
    '''
    images=[]
    for file in glob.glob(path+'/*.jpg'):
        images.append(file)
    return images

def make_thumb(path):
    '''
    获取图片的缩略图，file含路径
    '''
    filename, ext = os.path.splitext(os.path.basename(path))
    im = Image.open(path)
    im.thumbnail((200,200))
    im.save("{}_{}x{}.jpg".format('static/uploads/thumbs/'+filename,200,200),"JPEG")