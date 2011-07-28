#!/usr/bin/env python
import wsgiref.handlers
import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from django.utils import simplejson
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.api import images
from urllib import urlencode

#custom imports
import models
import geocode

class MainHandler(webapp.RequestHandler):
  def getNearby(self):
    user = users.get_current_user()
    logging.debug('start getNearby')
    profile = models.Profile.all().filter('user_id =',user.user_id()).get()
    lat = profile.location.lat
    lon = profile.location.lon
    #lat = self.request.get("lon")
    #lon = self.request.get("lat")

    preference = self.request.get("searchfor")
    if preference == 'w4m' or preference == 'w4w':
      gender = 'f'
    else:
      gender = 'm'

    if preference == 'w4w' or preference == 'm4w':
      wants = 'f'
    else:
      wants = 'm'

    max_distance = self.request.get("nearish")
    has_pic = self.request.get("haspic")
    last_online = self.request.get("online")
    logging.debug('search params: pref[' + preference + '] max_dist[' + max_distance + '] has_pic[' + has_pic + '] last_online[' + last_online + ']')

    mainHash = {} #main response hash
    profiles = models.Profile.proximity_fetch(
          models.Profile.all().filter('user_id !=',user.user_id()).filter('gender ==',gender).filter('wants ==',wants), 
          db.GeoPt(float(lat), float(lon)), 
          max_results=10)
    template_values = {
      "profiles" : profiles, 
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/rpc_table.html')
    templatehtml = template.render(path, template_values)
    mainHash["tablehtml"] = templatehtml
    return simplejson.dumps(mainHash)

  def getVenues(self):
    user = users.get_current_user()
    profile = models.Profile.all().filter('user_id =',user.user_id()).get()
    p_lat = profile.location.lat
    p_lon = profile.location.lon
    #TODO parse settings that might affect 
    #venue settings and types
    #but, for now, fuck it
    request_url = 'https://maps.googleapis.com/maps/api/place/search/json?location=' + str(p_lat) + ',' + str(p_lon) + '&radius=500&name=starbucks&sensor=false&key=AIzaSyD-wqm_olE-Dr374K2QT52xMNeuG1CaJVI'
    url_result = urlfetch.fetch(request_url)
    content = url_result.content
    json_decoder = simplejson.decoder.JSONDecoder()
    json = json_decoder.decode(content)
    results = json['results']
    template_values = {
        "venues" : results,
        }
    path = os.path.join(os.path.dirname(__file__), 'templates/rpc_venues.html')
    return template.render(path, template_values)

  def uploadPic(self):
    profile_id= self.request.get("profile_id")
    profile = models.Profile.get_by_id(int(profile_id))
    
    picFile = self.request.body
    if picFile != '':
      picBlob = models.PicBlob(blob = picFile)
      picBlob.put()
      picImg = images.Image(picFile)
      picImg.resize(width=80, height=100)
      thumb = picImg.execute_transforms(output_encoding=images.JPEG)
      thumbBlob = models.ThumbBlob(blob = thumb)
      thumbBlob.put()
      pic = models.Pic(picBlob = picBlob, thumbBlob = thumbBlob, profile = profile)
      pic.put()
      #return '<a href="/fullimg/' + str(pic.key().id()) + '"><img src="/thumb/'+ str(pic.key().id()) + '" /></a>'
      return simplejson.dumps({'success' : True})
    else:
      return simplejson.dumps({'success' : False, 'error' : 'dunno'})
    
    
  def get(self):
    self.request.path_info_pop()
    action = self.request.path_info_pop()
    
    if (action == 'nearby'):
      self.response.out.write(self.getNearby())

    if action == 'get_venues':
      self.response.out.write(self.getVenues())
      
  def post(self):
    self.request.path_info_pop()
    action = self.request.path_info_pop()
    if (action == 'pic'):
      self.response.out.write(self.uploadPic())

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([('/rpc.*', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
