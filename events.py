import webapp2
from master import Handler
from models import *

import time
import datetime

import logging

class List(Handler):
    def post(self):
        project_ids = self.request.get_all('project')
        project_ids = [int(x) for x in project_ids]
        project_keys = []
        for project_id in project_ids:
            project = Project.get_by_id(project_id)
            project_keys.append(project.key)
        events = Event.query(Event.project.IN(project_keys))
        self.render('partials/event_list.html', events = events)

class View(Handler):
    def get(self, event_id):
        event = Event.get_by_id(int(event_id))
        projects = Project.query().order(Project.created)
        collaborators = Collaborator.query()
        collaborator_list = []
        for collaborator in collaborators:
            collaborator_list.append(str(collaborator.email))
        self.render('event_view.html', projects = projects, event = event, collaborator_list = collaborator_list)

def process_emails(s):
    emails = s.split(',')
    emails = [email.strip() for email in emails]
    emails = [email for email in emails if email != ""]
    return emails

def get_fields(req, fields):
    data = {}
    for field in fields:
        data[field] = req.get(field)
    data['par'] = int(data['par'])
    formatstring = "%d/%m/%Y %I:%M %p"
    data['start'] = datetime.datetime.strptime(data['start'],
     formatstring)
    data['end'] = datetime.datetime.strptime(data['end'],
     formatstring)
    data['project'] = Project.get_by_id(
        int(data['project-id'])).key
    data['subproject'] = Subproject.get_by_id(
        int(data['subproject-id'])).key
    data['collaborators'] = process_emails(data['collaborators'])
    return data

class Create(Handler):
    def get(self):
        email = self.session.get('email')
        collaborators = Collaborator.query()
        projects = Project.query().order(Project.created)
        collaborator_list = []
        for collaborator in collaborators:
            collaborator_list.append(str(collaborator.email))
        self.render('event_create.html', projects = projects,
        collaborator_list = collaborator_list)
    def post(self):
        email = self.session['email']
        fields = ['project-id', 'subproject-id',
         'start', 'end', 'comments',
         'title', 'par', 'collaborators']
        data = get_fields(self.request, fields)
        event = Event(
            manager = email,
            title = data['title'],
            project = data['project'],
            subproject = data['subproject'],
            collaborator = data['collaborators'],
            start = data['start'],
            end = data['end'],
            par = data['par'],
            comments = data['comments']
            )
        # logging.info(data['collaborators'])
        event.put()
        time.sleep(.5)
        self.redirect('/')

class Update(Handler):
    def post(self, event_id):
        email = self.session.get('email')
        event = Event.get_by_id(int(event_id))
        fields = ['project-id', 'subproject-id',
         'start', 'end', 'comments',
         'title', 'par', 'collaborators']
        data = get_fields(self.request, fields)
        fields = ['title', 'project', 'subproject',
            'start', 'end', 'par', 'comments']
        for field in fields:
            setattr(event, field, data[field])
        setattr(event, 'collaborator', data['collaborators'])
        event.put()
        time.sleep(.5)
        self.redirect('/')

class Delete(Handler):
    def get(self, event_id):
        event = Event.get_by_id(int(event_id))
        event.key.delete()
        time.sleep(.5)
        self.redirect('/')
