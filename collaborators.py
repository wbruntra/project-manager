import webapp2
from master import Handler
from models import *

import time
import logging

class Manage(Handler):
    def get(self):
        email = self.session.get('email')
        collaborators = Collaborator.query().order(Collaborator.created)
        self.render('collaborators.html', collaborators = collaborators)

class View(Handler):
    def get(self, project_id):
        project = Project.get_by_id(int(project_id))
        subprojects = Subproject.query(
            Subproject.project == project.key)
        self.render('projectpage.html',
         project = project, subprojects = subprojects)

class Create(Handler):
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        admin = self.request.get('admin')
        admin = (admin == 'on')
        collaborator = Collaborator(name=name,
                        email=email,
                        admin=admin)
        collaborator.put()
        time.sleep(.5)
        self.redirect("/collaborators")

class Delete(Handler):
    def get(self, project_id):
        project = Project.get_by_id(int(project_id))
        events = Event.query(Event.project == project.key)
        subprojects = Subproject.query(Subproject.project == project.key)
        for event in events:
            event.key.delete()
        for subproject in subprojects:
            subproject.key.delete()
        project.key.delete()
        time.sleep(.5)
        self.redirect('/admin')
