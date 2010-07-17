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
		self.request.path_info_pop()
		postid = self.request.path_info_pop()
		
		post = models.Post.get_by_id(int(postid))
		replies = models.Reply.gql("WHERE post = :1" , post)
		
		postdata = {}
		replydata = []
		
		postdata["id"] = post.key().id()
		postdata["pic"] = post.pic.key().id()
		postdata["lat"] = post.location.lat
		postdata["lon"] = post.location.lon
		postdata["mod"] = post.modified
		
		for reply in replies:
			tmp = {}
			tmp["pic"] = reply.pic.key().id()
			tmp["desc"] = reply.content
			replydata.append(tmp)

		template_values = {
		'post': postdata,
		'replies': replydata
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/post.html')
		self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([
									('/post.*', MainHandler)
									],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
