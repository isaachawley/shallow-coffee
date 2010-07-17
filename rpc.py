#!/usr/bin/env python
import wsgiref.handlers
import os
import logging

from google.appengine.ext import webapp
#from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from django.utils import simplejson
from google.appengine.ext import webapp

#custom imports
import models
import geocode

class MainHandler(webapp.RequestHandler):
	def getNearby(self):
		lat = self.request.get("lon")
		lon = self.request.get("lat")
		mainHash = {} #main response hash
		mapHash = {} #map data hash
		posts = models.Post.proximity_fetch(
					models.Post.all(), 
					db.GeoPt(float(lon), float(lat)), 
					max_results=10)
		temps = []
		for p in posts:
			plocs = {} #dict for posts
			plocs["lon"] = p.location.lat
			plocs["lat"] = p.location.lon
			plocs["id"] = p.key().id().__str__()
			plocs["picid"] = p.pic.key().id().__str__()
			plocs["content"] = p.content
			mapHash[p.key().__str__()] = plocs
			temps.append(plocs)
			
		mainHash["mapdata"] = mapHash
		
		template_values = {
			"posts" : temps
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/rpc_table.html')
		templatehtml = template.render(path, template_values)
		mainHash["tablehtml"] = templatehtml
		return simplejson.dumps(mainHash)
		
	def get(self):
		self.request.path_info_pop()
		action = self.request.path_info_pop()
		
		if (action == 'nearby'):
			self.response.out.write(self.getNearby())
			
		def post(self):
			self.response.out.write("what?")

def main():
  application = webapp.WSGIApplication([('/rpc.*', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
