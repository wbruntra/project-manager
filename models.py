from google.appengine.ext import ndb

class Collaborator(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    admin = ndb.BooleanProperty()
    created = ndb.DateTimeProperty(auto_now_add = True)

class Project(ndb.Model):
    name = ndb.StringProperty()
    manager = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add = True)

class Subproject(ndb.Model):
    name = ndb.StringProperty()
    manager = ndb.StringProperty()
    project = ndb.KeyProperty(kind=Project, required=True)

class Event(ndb.Model):
    title = ndb.StringProperty()
    project = ndb.KeyProperty(kind=Project, required=True)
    subproject = ndb.KeyProperty(kind=Subproject, required=True)
    manager = ndb.StringProperty()
    collaborator = ndb.StringProperty(repeated = True)
    start = ndb.DateTimeProperty()
    end = ndb.DateTimeProperty()
    par = ndb.IntegerProperty()
    comments = ndb.TextProperty()
