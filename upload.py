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
	def newreply(self):
		postid = self.request.get("postid")
		post = models.Post.get_by_id(int(postid))
		
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
				pic = models.Pic(picBlob = picBlob, thumbBlob = thumbBlob)
				pic.put()
			except:
				self.response.out.write("<h1>Upload Failed</h1>")
				self.response.out.write("""
					<p>Your image may have been too big. Unfortunately there is a
					1 MB limit. You may need to resize your image.
					""")
				return
		else:
			pic = post.pic
		reply = models.Reply(content=self.request.get("desc"), pic = pic,
							post = post)
		reply.put()
		self.redirect('/post/' + postid)
	
	def newpost(self):
		if self.request.get("loctype") == "name":
			try:
				gc = geocode.GeoCode()
				locdata = gc.getCoords(self.request.get("loc"))
				coords = locdata["Placemark"][0]["Point"]["coordinates"]
				self.response.out.write(coords)
			except:
				self.response.out.write("<h1>Upload Failed</h1>")
				self.response.out.write("<p>Something is wrong with the location.")
				return
				
		elif self.request.get("loctype") == "coords":
			coordstring = self.request.get("loc")
			coords = coordstring.split(",")
		else:
			self.request.out.write("Wrong loctype")
			return
	
		
		picFile = self.request.get("file")
		if picFile != '':
			#avatar = images.resize(self.request.get("img"), 32, 32)
			#images.Image(photo.full_size_image)
			try:
				picBlob = models.PicBlob(blob = picFile)
				picBlob.put()
				picImg = images.Image(picFile)
				picImg.resize(width=80, height=100)
				thumb = picImg.execute_transforms(output_encoding=images.JPEG)
				thumbBlob = models.ThumbBlob(blob = thumb)
				thumbBlob.put()
				pic = models.Pic(picBlob = picBlob, thumbBlob = thumbBlob)
				pic.put()
			except:
				self.response.out.write("<h1>Upload Failed</h1>")
				self.response.out.write("""
					<p>Your image may have been too big. Unfortunately there is a
					1 MB limit. You may need to resize your image.
					""")
				return
		else:
			self.response.out.write("<h1>Pic required for new posts</h1>")
			return
		
		post = models.Post(location=db.GeoPt(float(coords[1]), float(coords[0])),
						content=self.request.get("desc"), pic=pic)
						
		post.update_location()
		post.put()

		reply = models.Reply(content=self.request.get("desc"), pic = pic,
							post = post)			
		reply.put()
		self.redirect('/post/' + post.key().id().__str__())
		
	def get(self):
		template_values = {
		'nothing':'nadda'
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/upload.html')
		self.response.out.write(template.render(path, template_values))

	
	def post(self):
		#picBlob = models.PicBlob()
		#picBlob.blob = db.Blob(self.request.get("file"))
		self.response.out.write('<h1><a href="/loc/place/98004/">// Loc // </a></h1><br>')
		if self.request.get("action") == "thread":
			self.newpost()
			
		elif self.request.get("action") == "reply":
			self.newreply()
		else:
			self.response.out.write("What?")
		
		

def main():
  application = webapp.WSGIApplication([('/upload.*', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
