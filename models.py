from google.appengine.ext import db
import geo.geomodel

class PicBlob(db.Model):
  blob = db.BlobProperty()
	
class ThumbBlob(db.Model):
  blob = db.BlobProperty()

class Profile(geo.geomodel.GeoModel):
  nick = db.StringProperty()
  joined = db.DateTimeProperty(auto_now=True)
  age = db.DateProperty()
  gender = db.StringProperty() # M F O
  wants = db.StringProperty() # M F MF OO
  email = db.StringProperty()

class Pic(db.Model):
  desc = db.StringProperty()
  picBlob = db.ReferenceProperty(PicBlob)
  thumbBlob = db.ReferenceProperty(ThumbBlob)
  profile = db.ReferenceProperty(Profile, collection_name='pictures')

