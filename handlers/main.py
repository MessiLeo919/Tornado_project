import tornado.web
import os

from utils import photo

class IndexHandler(tornado.web.RequestHandler):
    """
    Home page for user, photo feeds
    """
    def get(self, *args, **kwargs):
        images_path = os.path.join(self.settings.get('static_path'),'uploads')
        # print(self.settings.get('static_path'))
        images = photo.get_images(images_path)   #改目录下图片文件组成的列表，含路径
        self.render('index.html',
                    images=images)

class ExploreHandler(tornado.web.RequestHandler):
    """
    Explore page, photo of other users.
    """
    def get(self, *args, **kwargs):
        thumbs_path = os.path.join(self.settings.get('static_path'), 'uploads/thumbs')
        thumbs_images = photo.get_images(thumbs_path)
        # print("images-----",images)
        self.render('explore.html',
                    thumbsimages=thumbs_images)

class PostHandler(tornado.web.RequestHandler):
    """
    Single photo page, and maybe comments.
    """
    # def get(self, *args, **kwargs):
    #     self.render('post.html', post_idd=kwargs['post_id'])
    def get(self, post_id):
        self.render('post.html', post_idd=post_id)




class UploadHandler(tornado.web.RequestHandler):
    '''
    接收文件上传
    '''
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg',None)  #得到的是列表
        # print(img_files)
        for img_file in img_files:
            # print(img_file)
            with open('./static/uploads/'+img_file['filename'],'wb') as f:
                f.write(img_file['body'])
                # print("img_file{}".format(img_file))
            self.write({'got file': img_file['filename']})

            pic_path = os.path.join(self.settings.get('static_path'),'uploads/'+img_file['filename'])
            print("pic_path----",pic_path)

            photo.make_thumb(pic_path)


