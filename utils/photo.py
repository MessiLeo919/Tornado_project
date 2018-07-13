import os, uuid

from PIL import Image


class ImageSave(object):
    """

    """
    upload_dir = 'uploads'
    thumb_dir = 'thumbs'
    size = (200, 200)

    def __init__(self, static_path, old_name):
        self.static_path = static_path
        self.old_name = old_name
        self.new_name = self.gen_name()

    def gen_name(self):
        _, ext = os.path.splitext(self.old_name)
        return uuid.uuid4().hex + ext

    @property
    def upload_url(self):
        return os.path.join(self.upload_dir, self.new_name)

    @property
    def upload_path(self):
        return os.path.join(self.static_path, self.upload_url)

    def save_upload(self, content):
        with open(self.upload_path, 'wb') as f:
            f.write(content)

    @property
    def thumb_url(self):
        base, _ = os.path.splitext(self.new_name)
        thumb_name = os.path.join('{}_{}x{}.jpg'.
                                  format(base, self.size[0], self.size[1]))
        return os.path.join(self.upload_dir, self.thumb_dir, thumb_name)

    def make_thumb(self):
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        im.save(os.path.join(self.static_path, self.thumb_url), "JPEG")
