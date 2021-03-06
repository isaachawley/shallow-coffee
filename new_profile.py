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

class MainHandler(webapp.RequestHandler):
  def new_profile(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))

    try:
      gc = geocode.GeoCode()
      locdata = gc.getCoords(self.request.get("loc"))
      coords = locdata["Placemark"][0]["Point"]["coordinates"]
      self.response.out.write(coords)
    except:
      self.response.out.write("<h1>Upload Failed</h1>")
      self.response.out.write("<p>Something is wrong with the location.")
      return
        
    profile = models.Profile(
      location=db.GeoPt(
        float(coords[1]), 
        float(coords[0])),
      user_id = user.user_id(),
      )
            
    profile.update_location()
    profile.put()

    self.redirect('/profile/' 
        + profile.key().id().__str__() 
        + '/edit/details/')

  def get(self):
    default_lon = self.request.get("default_lon")
    default_lat = self.request.get("default_lat")

    template_values = {
      'default_lon':default_lon,
      'default_lat':default_lat,
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/pick_loc.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    if self.request.get("action") == "location":
      self.new_profile()
    else:
      self.response.out.write("What?")
    
    

def main():
  application = webapp.WSGIApplication([('/new_profile.*', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
