import tornado.web

from utils.account import authenticate, register, login
from .main import AuthBaseHandler


class LoginHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        if self.current_user:
            self.redirect('/')
        self.render('login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        print('username', username)
        print('password', password)
        passed = authenticate(username, password)

        if passed:
            self.session.set('bayern_user_info', username)
            login(username)

            self.redirect('/')
        # self.write('Login OK!')
        else:
            self.write('msg:login fail')


class LogoutHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.session.set('bayern_user_info', '')
        self.redirect('/login')


class SignupHandler(AuthBaseHandler):

    def get(self, *args, **kwargs):
        self.render('signup.html', msg = '')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')

        if username and password1 and password2:
            if password1 != password2:
                # self.write({'msg':'两次输入的密码不匹配'}.decode())
                self.write('两次输入的密码不匹配')
            else:
                ret = register(username, password1, email)
                if ret['msg'] == 'OK':
                    self.session.set('bayern_user_info', username)
                    self.redirect('/')
                else:
                    self.write(ret)
        else:
            self.render('signup.html', msg = {'register' : 'fail'})
