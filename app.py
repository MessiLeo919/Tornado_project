import os.path

import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from handlers import main


define('port', default='8000', help='Listening port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', main.IndexHandler),
            ('/explore', main.ExploreHandler),
            ('/post/(?P<post_id>[0-9]+)', main.PostHandler),
            ('/upload', main.UploadHandler),

        ]
        settings = dict(
            debug=True,
            template_path = os.path.join(os.path.dirname(__file__), 'templates')
        )
        super(Application, self).__init__(handlers,**settings)  #**是将字典拆包

application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()  #打印请求行信息
    application.listen(options.port)
    print("Server starts on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()  #current()也可以换成instance()
