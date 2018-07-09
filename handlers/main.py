import tornado.web
import os
from pycket.session import SessionMixin

from utils import photo


class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        return self.session.get('bayern_user_info')


class IndexHandler(AuthBaseHandler):
    """
    Home page for user, photo feeds
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # print("**************")
        images_path = os.path.join(self.settings.get('static_path'), 'uploads')
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
        img_files = self.request.files.get('newimg', None)  #得到的是列表
        for img_file in img_files:
            with open('./static/uploads/' + img_file['filename'], 'wb') as f:
                f.write(img_file['body'])
            pic_path = os.path.join(self.settings.get('static_path'), 'uploads/'+img_file['filename'])

            photo.make_thumb(pic_path)

            self.write({'got file': img_file['filename']})
