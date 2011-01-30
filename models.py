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
  user_id = db.StringProperty() #assoc with google account

class Pic(db.Model):
  desc = db.StringProperty()
  picBlob = db.ReferenceProperty(PicBlob)
  thumbBlob = db.ReferenceProperty(ThumbBlob)
  profile = db.ReferenceProperty(Profile, collection_name='pictures')

#class Venue(geo.geomodel.GeoModel):
class Venue(db.Model):
  name = db.StringProperty()
  desc = db.StringProperty()

class Invited(db.Model):
  inviter = db.ReferenceProperty(Profile, collection_name = 'inviters')
  invitee = db.ReferenceProperty(Profile, collection_name = 'invitees')
  invited_date = db.DateTimeProperty(auto_now=True)
  date_date_1 = db.DateTimeProperty(auto_now=True)
  date_date_2 = db.DateTimeProperty(auto_now=True)
  date_date_3 = db.DateTimeProperty(auto_now=True)
  venue = db.ReferenceProperty(Venue)

class Accepted(db.Model):
  inviter = db.ReferenceProperty(Profile, collection_name = 'inviters_accepted')
  invitee = db.ReferenceProperty(Profile, collection_name = 'invitees_accepted')
  invited_date = db.DateTimeProperty(auto_now=True)
  accepted_date = db.DateTimeProperty(auto_now=True)
  date_date = db.DateTimeProperty(auto_now=True)
  venue = db.ReferenceProperty(Venue)


class Invite_Archive(db.Model):
  inviter = db.ReferenceProperty(Profile, collection_name = 'inviters_archived')
  invitee = db.ReferenceProperty(Profile, collection_name = 'invitees_archived')
  invited_date = db.DateTimeProperty(auto_now=True)
  date_date = db.DateTimeProperty(auto_now=True)
  venue = db.ReferenceProperty(Venue)
  result = db.StringProperty()
