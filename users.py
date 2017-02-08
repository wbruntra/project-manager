import hashlib
import hmac
import random
from google.appengine.ext import ndb
from string import letters

from master import Handler
import time

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
    name = ndb.StringProperty()
    pw_hash = ndb.StringProperty()
    restrict = ndb.IntegerProperty()
    registered = ndb.BooleanProperty()
    created = ndb.DateTimeProperty(auto_now_add = True)

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

class Initialize(Handler):
    def get(self):
        email = "bill.bruntrager@gmail.com"
        password = "secret"
        restrict = 0
        user = User.register(email, password)
        user.restrict = restrict
        user.registered = True
        user.name = "Bill Bruntrager"
        user.put()
        self.redirect('/')

class Add(Handler):
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        admin = self.request.get('admin')
        if (admin == 'on'):
            restrict = 0
        else:
            restrict = 1
        user = User(name = name,
                    email = email,
                    restrict = restrict,
                    registered = False)
        user.put()
        time.sleep(.5)
        self.redirect("/collaborators")

class Register(Handler):
    def get(self):
        self.render('register.html')
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        c = User.by_email(email)
        if not c:
            self.render('bad-registration.html')
        else:
            pw_hash = make_pw_hash(email, password)
            c.registered = True
            c.pw_hash = pw_hash
            c.put()
            self.session['email'] = email
            self.session['restrict'] = c.restrict
            self.redirect('/')

class Change(Handler):
    def get(self):
        email = self.session['email']
        user = User.by_email(email)
        self.render('profile-edit.html', user = user)
    def post(self):
        email = self.session['email']
        old_pw = self.request.get('old_pw')
        new_pw = self.request.get('password')
        u = User.login(email, old_pw)
        if not u:
            self.write('Incorrect password!')
        else:
            pw_hash = make_pw_hash(email, new_pw)
            u.pw_hash = pw_hash
            u.put()
            self.redirect('/')

class Login(Handler):
    def get(self):
        self.render('login.html')
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        c = User.by_email(email)
        if not c:
            self.render('bad-registration.html')
        elif not c.registered:
            self.write('You need to register an account first.')
        else:
            u = User.login(email, password)
            if u:
                self.session['email'] = self.request.get('email')
                self.session['restrict'] = u.restrict
                self.redirect("/")
            else:
                self.write("Invalid credentials!")

class Logout(Handler):
    def get(self):
        del self.session['email']
        self.redirect('/login')
