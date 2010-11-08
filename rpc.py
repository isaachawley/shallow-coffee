#!/usr/bin/env python
import wsgiref.handlers
import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from django.utils import simplejson
from google.appengine.ext import webapp

#custom imports
import models
import geocode

class MainHandler(webapp.RequestHandler):
  def getNearby(self):
    user = users.get_current_user()
    logging.debug('start getNearby')
    lat = self.request.get("lon")
    lon = self.request.get("lat")
    logging.debug('getNearby lon[' + lon + '] lat[' + lat + ']')
    mainHash = {} #main response hash
    mapHash = {} #map data hash
    profiles = models.Profile.proximity_fetch(
          models.Profile.all().filter('user_id !=',user.user_id()), 
          db.GeoPt(float(lon), float(lat)), 
          max_results=10)

    for p in profiles:
      plocs = {} #dict for profiles
      plocs["lon"] = p.location.lat
      plocs["lat"] = p.location.lon
      plocs["id"] = p.key().id().__str__()
      if (p.pictures.count() > 0):
        plocs["picid"] = p.pictures[0].key().id().__str__()
      #plocs["content"] = p.content
      plocs["nick"] = p.nick
      logging.debug('getNearby adding[' + p.nick + '] to maphash')
      mapHash[p.key().__str__()] = plocs
      
    mainHash["mapdata"] = mapHash

    template_values = {
      "profiles" : profiles, 
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/rpc_table.html')
    templatehtml = template.render(path, template_values)
    mainHash["tablehtml"] = templatehtml
    return simplejson.dumps(mainHash)

  def uploadPic(self):
    profile_id= self.request.get("profile_id")
    profile = models.Profile.get_by_id(int(profile_id))
    
    picFile = self.request.get("file")
    if picFile != '':
      try:
        picBlob = models.PicBlob(blob = picFile)
        picBlob.put()
        picImg = images.Image(picFile)
        picImg.resize(width=80, height=100)
        thumb = picImg.execute_transforms(output_encoding=images.JPEG)
        thumbBlob = models.ThumbBlob(blob = thumb)
        thumbBlob.put()
        pic = models.Pic(picBlob = picBlob, thumbBlob = thumbBlob, profile = profile)
        pic.put()
      except:
        self.response.out.write("<h1>Upload Failed</h1>")
        self.response.out.write("""
          <p>Your image may have been too big. Unfortunately there is a
          1 MB limit. You may need to resize your image.
          """)
        return
    return '<div> uploadPic NYI </div>'
    
    
  def get(self):
    self.request.path_info_pop()
    action = self.request.path_info_pop()
    
    if (action == 'nearby'):
      self.response.out.write(self.getNearby())
      
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
