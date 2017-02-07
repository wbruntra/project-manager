import webapp2
from master import Handler
from models import *

import time


def get_subprojects(project_id):
    project_id = int(project_id)
    project = Project.get_by_id(project_id)
    subprojects = Subproject.query(
        Subproject.project == project.key)
    return subprojects

class Manage(Handler):
    def get(self):
        email = self.session.get('email')
        projects = Project.query().order(Project.created)
        data = {}
        for project in projects:
            subprojects = Subproject.query(
                Subproject.project == project.key
            )
            data[project.key] = subprojects
        self.render('admin_page.html', projects = projects, data = data)

class Edit(Handler):
    def get(self):
        projects = Project.query().order(Project.created)
        self.render('edit-projects.html', projects = projects)

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
        manager = self.session.get('email')
        project = Project(name=name,
                        manager=manager)
        project.put()
        time.sleep(.5)
        self.redirect("/admin")

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
        self.redirect('/projects/edit')
