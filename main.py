#!/usr/bin/env python

import os

import jinja2
import webapp2

from google.appengine.ext import ndb

import json
import time

import logging

class Animal(ndb.Model):
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add = True)

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = False)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'

class MainHandler(Handler):
    def get(self):
        # this is the line you will change
        self.render('main.html')

class GreetingHandler(Handler):
    def get(self, name):
        self.write("Hello, %s" % (name))

class AnimalHandler(Handler):
    def get(self):
        # import pdb; pdb.set_trace()
        animals = Animal.query().fetch()
        if self.format == "json":
            o = []
            for animal in animals:
                o.append({"name": animal.name })
            msg = json.dumps(o)
            self.response.headers.add_header('Content-Type', "application/json")
            self.write(msg)
        else:
            self.render('animals.html', animals = animals)
    def post(self):
        name = self.request.get('name')
        animal = Animal(name = name)
        animal.put()
        time.sleep(.5)
        self.redirect('/animals')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/greet/(.*)', GreetingHandler),
    ('/animals(?:.json)?', AnimalHandler)
], debug=True)
