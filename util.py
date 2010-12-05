#!/usr/bin/env python
from google.appengine.api import users 

def create_logout_url(url):
  return users.create_logout_url(url)
  
