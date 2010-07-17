from google.appengine.ext import db
import geo.geomodel

class PicBlob(db.Model):
	#name
	blob = db.BlobProperty()
	
class ThumbBlob(db.Model):
	blob = db.BlobProperty()

class Pic(db.Model):
	title = db.StringProperty()
	desc = db.StringProperty()
	picBlob = db.ReferenceProperty(PicBlob)
	thumbBlob = db.ReferenceProperty(ThumbBlob)
	#location property
	
class Post(geo.geomodel.GeoModel):
	#location from geomodel
	#copy of the initial reply data
	#	so that we dont have to double fetch initially
	content = db.StringProperty()
	modified = db.DateTimeProperty(auto_now=True)
	pic = db.ReferenceProperty(Pic)

class Reply(db.Model):
	#the post
	pic = db.ReferenceProperty(Pic) #to a picture
	content = db.StringProperty()
	post = db.ReferenceProperty(Post) #to a post
	modified = db.DateTimeProperty(auto_now=True)
	
