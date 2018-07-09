import os.path
import time
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from handlers import main
from handlers import auth


define('port', default='8000', help='Listening port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', main.IndexHandler),
            ('/explore', main.ExploreHandler),
            ('/post/(?P<post_id>[0-9]+)', main.PostHandler),
            ('/upload', main.UploadHandler),
            ('/login', auth.LoginHandler),
            ('/logout', auth.LogoutHandler),
            ('/signup', auth.SignupHandler),

        ]
        settings = dict(
            debug=True,
            template_path = os.path.join(os.path.dirname(__file__), 'templates'),
            static_path = os.path.join(os.path.dirname(__file__), 'static'),
            login_url = '/login',
            cookie_secret = 'ajfjowjr343',
            pycket = {
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    'db_sessions': 5,
                    'db_notifications': 11,
                    'max_connections': 2**30,
                },
                'cookies': {
                    'expires': time.time() + 180,
                }
            }
        )
        super(Application, self).__init__(handlers, **settings)  #**是将字典拆包


application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()  #打印请求行信息
    application.listen(options.port)
    print("Server starts on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()  #current()也可以换成instance()
