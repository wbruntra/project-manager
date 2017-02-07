import webapp2
from master import Handler
from models import *
from users import User

import time
import logging

class Manage(Handler):
    def get(self):
        email = self.session.get('email')
        collaborators = User.query().order(User.created)
        self.render('collaborators.html', collaborators = collaborators)
