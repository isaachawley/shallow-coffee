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

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.request.path_info_pop()
    profileid = self.request.path_info_pop()
    action = self.request.path_info_pop()

    if (action == 'view'):
      profile = models.Profile.get_by_id(int(profileid))
      pictures = profile.pictures
      inviters = profile.inviters
      invitees = profile.invitees

      #when this profile did the inviting, is the inviter
      for inviter in inviters:
        self.response.out.write('invitee:' + inviter.invitee.nick + '<br>')

      #when this profile is the invitee
      # profile.i'm the invitee.this is confusing =(
      for invitee in invitees:
        self.response.out.write('invitee.inviter:' + invitee.inviter.nick + '<br>')
        self.response.out.write('invitee.invitee:' + invitee.invitee.nick + '<br>')

      #the collection names are confusing and I should change them

      template_values = {
            'profile' : profile,
            'pictures' : pictures,
          }

      path = os.path.join(
          os.path.dirname(__file__), 
          'templates/view_profile.html'
          )
      self.response.out.write(template.render(path, template_values))

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

    if (action == 'invite'):
      user = users.get_current_user()
      if not user:
        self.redirect(users.create_login_url(self.request.uri))
      askee = models.Profile.get_by_id(int(profileid))
      template_values = {
        'profileid' : profileid,
      }
      path = os.path.join(os.path.dirname(__file__), 'templates/schedule_form.html')
      self.response.out.write(template.render(path, template_values))



    if (action == 'accept'):
      user = users.get_current_user()
      if not user:
        self.redirect('/')
      accepter = models.Profile.all().filter('user_id ==',user.user_id()).fetch(1)[0]
      acceptee = models.Profile.get_by_id(int(profileid))
      invitation = accepter.invitees.filter('inviter =', acceptee.key()).fetch(1)[0]
      
      accepted = models.Accepted(inviter = invitation.inviter, invitee = invitation.invitee, invited_date = invitation.invited_date, venue = invitation.venue)

      invitation.delete()
      accepted.put()
      self.redirect('/home')

  def post(self):
    self.request.path_info_pop()
    profileid = self.request.path_info_pop()
    action = self.request.path_info_pop()

    if (action == 'ask'):
      user = users.get_current_user()
      if not user:
        self.redirect(users.create_login_url(self.request.uri))
      asker = models.Profile.all().filter('user_id ==',user.user_id()).fetch(1)[0]
      askee = models.Profile.get_by_id(int(profileid))
      venues = models.Venue.all()
      for venuea in venues:
        venue = venuea

      invitation = models.Invited(inviter = asker, invitee = askee, venue = venue)
      invitation.put()
      #self.response.out.write('invitation successful')
      self.redirect('/profile/' + profileid + '/view')

    if (action == 'edit'):
      what = self.request.path_info_pop()
      self.response.out.write('do[' + action + '] on[' + what + ']')

      profile = models.Profile.get_by_id(int(profileid))

      profile.nick = self.request.get('nick')
      #profile.age = int(self.request.get('age'))
      # date stuff ugh :(
      profile.gender = self.request.get('gender')
      profile.wants = self.request.get('wants')
      profile.put()


def main():
  application = webapp.WSGIApplication([
									('/profile.*', MainHandler)
									],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
