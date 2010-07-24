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
from google.appengine.api import images

#custom imports
import models
import geocode

class MainHandler(webapp.RequestHandler):
		
	def get(self):
		template_values = {
		'nothing':'nadda'
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/upload.html')
		self.response.out.write(template.render(path, template_values))

	def post(self):
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

		self.redirect('/profile/' + profile_id + '/view')
	
def main():
  application = webapp.WSGIApplication([('/upload_pic.*', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
