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
		self.redirect('/loc/place/Malaysia/')

class Loc(webapp.RequestHandler):
	def get(self):
		self.request.path_info_pop()
		loctype = self.request.path_info_pop()
		if loctype == "place":
			locstring = self.request.path_info_pop()
		
			gc = geocode.GeoCode()
			locdata = gc.getCoords(locstring)
			try:
				coords = locdata["Placemark"][0]["Point"]["coordinates"]
			except:
				#47.6264794,-122.2051487
				coords = (-122.2051487, 47.6264794)
		
		elif loctype == "coords":
			lat = self.request.path_info_pop()
			lon = self.request.path_info_pop()
			coords = (float(lat), float(lon)) 
		else:
			self.response.out.write("""<h1>Bad loctype</h1>
				<p>Options are /place/ or /coords/</p>
			
			""")
			return
		
		template_values = {
		"center_lat" : coords[0],
		"center_lon" : coords[1]
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/loc.html')
		self.response.out.write(template.render(path, template_values))

class Test(webapp.RequestHandler):
	def get(self):
		self.response.out.write(self.request)
		
class Latest(webapp.RequestHandler):
	def get(self):
		q = models.Post.gql("ORDER BY modified DESC")
		results = q.fetch(10)
		ph = []
		for p in results:
			pt = {}
			pt['id'] = str(p.key().id())
			pt['picid'] = str(p.pic.key().id())
			pt['content'] = p.content
			ph.append(pt)
			
		template_values = {
			"posts" : ph
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/rpc_table.html')
		self.response.out.write(template.render(path, template_values))

class Updater(webapp.RequestHandler):
	def get(self):
		#posts = models.Post.all()
		#for p in posts:
		#	p.put()
			
		self.response.out.write("no more updating")

def main():
  application = webapp.WSGIApplication([
									('/', MainHandler),
									('/loc.*', Loc),
									('/test/.*', Test),
									('/latest.*', Latest),
									('/updateModels.*', Updater)
									],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
