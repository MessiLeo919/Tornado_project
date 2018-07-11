import os
import glob

from PIL import Image


class ImageSave(object):
    """

    """
    upload_dir = 'uploads'
    thumb_dir = 'thumbs'
    size = (200, 200)

    def __init__(self, static_path, name):
        self.static_path = static_path
        self.name = name

    @property
    def upload_url(self):
        return os.path.join(self.upload_dir, self.name)

    @property
    def upload_path(self):
        return os.path.join(self.static_path, self.upload_url)

    def save_upload(self, content):
        with open(self.upload_path, 'wb') as f:
            f.write(content)

    @property
    def thumb_url(self):
        base, _ = os.path.splitext(self.name)
        thumb_name = os.path.join('{}_{}x{}.jpg'.
                                  format(base, self.size[0], self.size[1]))
        return os.path.join(self.upload_dir, self.thumb_dir, thumb_name)

    def make_thumb(self):
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        im.save(os.path.join(self.static_path, self.thumb_url), "JPEG")




