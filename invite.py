#!/usr/bin/env python
import wsgiref.handlers
import os
from datetime import datetime, date, time 
from google.appengine.ext import webapp
from google.appengine.api import users 
from google.appengine.ext import db
from google.appengine.ext.webapp import template

#custom imports
import models
import geocode
import geo.geotypes

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.request.path_info_pop()
    inviteid = self.request.path_info_pop()
    action = self.request.path_info_pop()

    if (action == 'cancel'):
      user = users.get_current_user()
      if not user:
        self.redirect('/')

      invite = models.Invited.get_by_id(int(inviteid))
      #check if valid invitation at some point
      invite.delete()
      self.redirect('/home/')

    #path = os.path.join(
    #    os.path.dirname(__file__), 
    #    'templates/view_invite.html'
    #    )
    #self.response.out.write(template.render(path, template_values))



#  def post(self):

def main():
  application = webapp.WSGIApplication([
									('/invite.*', MainHandler)
									],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
