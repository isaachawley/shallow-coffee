#!/usr/bin/env python

import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext import db

#custom imports
import models

class MainHandler(webapp.RequestHandler):
	
	def get(self):
		self.request.path_info_pop()
		self.response.out.write("<img src='/image/" + self.request.path_info_pop() + "'>")
		
def main():
	application = webapp.WSGIApplication([('/fullimg.*', MainHandler)],
	                                       debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()