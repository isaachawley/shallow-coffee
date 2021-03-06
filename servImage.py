#!/usr/bin/env python

import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext import db

#custom imports
import models

class MainHandler(webapp.RequestHandler):
	
	def get(self):
		self.request.path_info_pop()
		pic = models.Pic.get_by_id(int(self.request.path_info_pop()))
		self.response.headers['Content-Type'] = "image/png"
		self.response.out.write(pic.picBlob.blob)
		
def main():
	application = webapp.WSGIApplication([('/image.*', MainHandler)],
	                                       debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
