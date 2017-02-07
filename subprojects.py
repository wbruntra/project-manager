import webapp2
from master import Handler
from models import *

import time

class View(Handler):
    def get(self, event_id):
        self.write('Nothing yet')

class Create(Handler):
    def post(self):
        project_id = self.request.get('project-id')
        project = Project.get_by_id(int(project_id))
        name = self.request.get('name')
        subproject = Subproject(name=name,
                        project=project.key)
        subproject.put()
        time.sleep(.5)
        self.redirect('/admin')

class Delete(Handler):
    def get(self, subproject_id):
        subproject = Subproject.get_by_id(int(subproject_id))
        events = Event.query(Event.subproject == subproject.key)
        for event in events:
            event.key.delete()
        subproject.key.delete()
        time.sleep(.5)
        self.redirect('/admin')
