import webapp2
import os, sys
from master import Handler

import httplib2

from googleapiclient import discovery
from oauth2client import client
from oauth2client.contrib import appengine
from google.appengine.api import memcache

SCOPE = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
APPLICATION_NAME = 'New Google Calendar'

http = httplib2.Http(memcache)
service = discovery.build("calendar", "v3", http=http)
decorator = appengine.oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope=SCOPE,
    message="Missing Client Secrets")

class EventListing(Handler):
    @decorator.oauth_required
    def get(self):
        try:
            http = decorator.http()
            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            eventsResult = service.events().list(
                calendarId='33bl8lt5urt9j5vltlrn54qrv0@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
                orderBy='startTime').execute(http=http)
            events = eventsResult.get('items', [])
            self.render('events.html', events = events)
        except client.AccessTokenRefreshError:
            self.redirect('/')

class CalendarList(Handler):
    @decorator.oauth_required
    def get(self):
        try:
            http = decorator.http()
            calendarsResult = service.calendarList().list(
                fields="items(id,summary)"
            ).execute(http=http)
            calendars = calendarsResult.get('items',[])
            self.render('calendars.html', calendars = calendars)
        except client.AccessTokenRefreshError:
            self.redirect('/')

class FulfordEvents(Handler):
    @decorator.oauth_required
    def get(self):
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            calendarIds = []
            events = []
            http = decorator.http()
            calendarsResult = service.calendarList().list(
                fields="items(id,summary)"
            ).execute(http=http)
            calendars = calendarsResult.get('items',[])
            for calendar in calendars:
                name = calendar['summary']
                if name.find('Fulford') != -1:
                    calendarIds.append(calendar['id'])
            logging.info("Calendars: "+ str(calendarIds))
            for calendarId in calendarIds:
                eventsResult = service.events().list(
                    calendarId=calendarId,
                    timeMin=now,
                    maxResults=50).execute(http=http)
                new_events = eventsResult.get('items', [])
                events = events + new_events
            self.render('events.html', events = events)
        except client.AccessTokenRefreshError:
            self.redirect('/')
