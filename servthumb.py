#!/usr/bin/env python

import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext import db

#custom imports
import models

class MainHandler(webapp.RequestHandler):
	
	def get(self):
		#self.response.headers['Content-Type'] = 'image/jpeg'
		self.request.path_info_pop()
		pic = models.Pic.get_by_id(int(self.request.path_info_pop()))
		self.response.out.write(pic.thumbBlob.blob)
		
def main():
	application = webapp.WSGIApplication([('/thumb.*', MainHandler)],
	                                       debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()