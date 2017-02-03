import hashlib
import hmac
import random
from google.appengine.ext import ndb
from string import letters

from master import Handler

##### user stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

class User(ndb.Model):
    email = ndb.StringProperty(required= True)
    pw_hash = ndb.StringProperty(required = True)

    @classmethod
    def by_email(cls, email):
        u = User.query(User.email == email).get()
        return u

    @classmethod
    def register(cls, email, pw):
        pw_hash = make_pw_hash(email, pw)
        return User(pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, email, pw):
        u = cls.by_email(email)
        if u and valid_pw(email, pw, u.pw_hash):
            return u

class Register(Handler):
    def get(self):
        self.render('register.html')
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        user = User.register(email, password)
        user.put()
        self.session['email'] = email
        self.redirect('/')

class Login(Handler):
    def get(self):
        self.render('login.html')
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        u = User.login(email, password)
        if u:
            self.session['email'] = self.request.get('email')
            self.redirect("/")
        else:
            self.write("Invalid credentials!")

class Logout(Handler):
    def get(self):
        del self.session['email']
        self.redirect('/login')
