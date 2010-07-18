#!/usr/bin/env python
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

#custom imports
import models
import geocode
import geo.geotypes

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.request.path_info_pop()
    profileid = self.request.path_info_pop()
    action = self.request.path_info_pop()

    if (action == 'view'):
      profile = models.Profile.get_by_id(int(profileid))
      self.response.out.write("nick["+profile.nick+"] age[] gender["+profile.gender+"] wants["+profile.wants+"] ")

    if (action == 'edit'):
      what = self.request.path_info_pop()
      self.response.out.write('do[' + action + '] on[' + what + ']')

      profile = models.Profile.get_by_id(int(profileid))

      profiledata = {}

      profiledata["id"] = profile.key().id()
      profiledata["lat"] = profile.location.lat
      profiledata["lon"] = profile.location.lon

      template_values = {
      'profile': profiledata,
      'profileid' : profileid,
      }
      path = os.path.join(os.path.dirname(__file__), 'templates/edit_profile_details.html')
      self.response.out.write(template.render(path, template_values))

  def post(self):
    self.request.path_info_pop()
    profileid = self.request.path_info_pop()
    action = self.request.path_info_pop()

    if (action == 'edit'):
      what = self.request.path_info_pop()
      self.response.out.write('do[' + action + '] on[' + what + ']')

    profile = models.Profile.get_by_id(int(profileid))

    profile.nick = self.request.get('nick')
    #profile.age = self.request.get('age')
    profile.gender = self.request.get('gender')
    profile.wants = self.request.get('wants')
    profile.put()
    self.redirect('/profile/' + profileid + '/view')


def main():
  application = webapp.WSGIApplication([
									('/profile.*', MainHandler)
									],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
