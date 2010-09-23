#!/usr/bin/env python
import wsgiref.handlers
import os
import logging

from google.appengine.ext import webapp
#from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from django.utils import simplejson
from google.appengine.api import users 
from google.appengine.ext import webapp
from google.appengine.api import images

#custom imports
import models
import geocode

class NewHandler(webapp.RequestHandler):
  def new_venue(self):
    venue = models.Venue(
        name = self.request.get('name'),
        desc = self.request.get('desc'),
      )
    venue.put()

    self.redirect('/venue/' 
        + venue.key().id().__str__() 
        + '/')

  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'templates/new_venue.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    self.new_venue()

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.request.path_info_pop()
    venueid = self.request.path_info_pop()

    venue = models.Venue.get_by_id(int(venueid))
    
    template_values = {
        'venue' : venue,
        }
    path=os.path.join(os.path.dirname(__file__),'templates/view_venue.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/new_venue.*', NewHandler),
                                        ('/venue.*',MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
