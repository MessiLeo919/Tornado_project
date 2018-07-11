import tornado.web
import os
from pycket.session import SessionMixin

from utils import photo
from utils.account import add_post_for, get_post_for


class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('bayern_user_info')


class IndexHandler(AuthBaseHandler):
    """
    Home page for user, photo feeds，大图
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # print(self.settings.get('static_path'))
        posts = get_post_for(self.current_user)   # 改目录下图片文件组成的列表，含路径
        image_urls = [p.image_url for p in posts]
        self.render('index.html',
                    images=image_urls)


class ExploreHandler(AuthBaseHandler):
    """
    Explore page, photo of other users.缩略图
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = get_post_for(self.current_user)  # 改目录下图片文件组成的列表，含路径
        thumb_urls = [p.thumb_url for p in posts]
        self.render('explore.html',
                    thumbsimages=thumb_urls)


class PostHandler(tornado.web.RequestHandler):
    """
    Single photo page, and maybe comments.
    """
    def get(self, post_id):
        self.render('post.html', post_idd=post_id)


class UploadHandler(AuthBaseHandler):
    """
    接收文件上传
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg', None)  # 得到的是列表
        for img_file in img_files:
            saver = photo.ImageSave(self.settings['static_path'],
                                    img_file['filename'])
            saver.save_upload(img_file['body'])
            saver.make_thumb()
            add_post_for(self.current_user, saver.upload_url, saver.thumb_url)
            print("save to {}".format(saver.upload_path))
        self.redirect('/explore')
