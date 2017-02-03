#!/usr/bin/env python

import os

import jinja2
import webapp2

import json
import time
import datetime

import logging

from webapp2_extras import sessions

from secrets import SESSION_KEY

from master import Handler
from users import User
import events
import subprojects
import projects
import users
import collaborators

from models import *
from googlehandlers import decorator
from projects import get_subprojects

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'ezOhxK7i41amGYUbLC5C',
}

class MainHandler(Handler):
    def get(self):
        email = self.session.get('email')
        if not email:
            self.redirect('/login')
        projects = Project.query().order(Project.created)
        events = Event.query().order(Event.end)
        self.render('index.html',
            projects = projects,
            events = events)

class RetrieveSubprojects(Handler):
    def get(self, project_id):
        # email = self.session['email']
        subprojects = get_subprojects(project_id)
        message = []
        for sp in subprojects:
            o = {'name': sp.name,
                'id':sp.key.id()}
            message.append(o)
        self.render('partials/select.html',
         subprojects=subprojects);

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/admin', projects.Manage),
    ('/events/create', events.Create),
    ('/events/project', events.List),
    ('/events/view/([0-9]+)', events.View),
    ('/events/update/([0-9]+)', events.Update),
    ('/events/delete/([0-9]+)', events.Delete),
    ('/projects/create', projects.Create),
    ('/projects/delete/([0-9]+)', projects.Delete),
    ('/projects/manage/([0-9]+)', projects.View),
    ('/subprojects/create', subprojects.Create),
    ('/subprojects/delete/([0-9]+)', subprojects.Delete),
    ('/collaborators', collaborators.Manage),
    ('/collaborators/add', collaborators.Create),
    ('/login', users.Login),
    ('/register', users.Register),
    ('/logout', users.Logout),
    ('/api/get/subprojects/([0-9]+)', RetrieveSubprojects),
    (decorator.callback_path, decorator.callback_handler()),
], config=config, debug=True)
