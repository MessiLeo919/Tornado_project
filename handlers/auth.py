import tornado.web

from utils.account import authenticate, register, login_time_update
from .main import AuthBaseHandler


class LoginHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        if self.current_user:
            self.redirect('/')
        next = self.get_argument('next','')
        self.render('login.html', next = next)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        passed = authenticate(username, password)

        if passed:
            self.session.set('bayern_user_info', username)
            print('设置cookie成功')
            login_time_update(username)
            print("登录成功Hello!", self.get_argument('next', '/'))
            if self.get_argument('next', '/'):
                self.redirect(self.get_argument('next', '/'))
            else:
                self.redirect('/')
        else:
            self.write('msg:login fail')


class LogoutHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.session.delete('bayern_user_info')
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
