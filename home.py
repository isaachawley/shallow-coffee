#!/usr/bin/env python
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.api import users 
from google.appengine.ext import db
from google.appengine.ext.webapp import template

#custom imports
import models
import geocode
import geo.geotypes
import util

class MainHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))

    profile = models.Profile.all().filter('user_id =',user.user_id()).get()
    if not profile:
      self.redirect('/new_profile')
      return

    path = os.path.join(os.path.dirname(__file__), 'templates/upload_pic.html')
    addpic_html = template.render(path, {'profileid' : profile.key().id()})

    template_values = {
        'logout' : util.create_logout_url(''),
        'profile' : profile,
        'pictures' : profile.pictures,
        'inviters' : profile.inviters,
        'invitees' : profile.invitees,
        'accepters' : profile.inviters_accepted,
        'acceptees' : profile.invitees_accepted,
        'addpic_html' : addpic_html,
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([
									('/home.*', MainHandler),
									],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
