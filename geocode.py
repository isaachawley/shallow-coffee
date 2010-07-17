#!/usr/bin/env python
import urllib, urllib2
from django.utils import simplejson

class GeoCode():
	
	def getCoords(self, stringloc):
		baseUrl = "http://maps.google.com/maps/geo?"
		#baseUrl = "http://localhost:8080/test/"
		apiKey = "ABQIAAAAGGMJIuUzby07NUrR7mallhRzMbK_vc1IJzc6XHaFszlH54JBnhSVeGU5h8-LsX0JY8fEk5y5pYPqbw"
		values = {"q": stringloc, "output":"json", "sensor":"false", "key":apiKey}
		params = urllib.urlencode(values)
		result = urllib2.urlopen(baseUrl + params)
		jsonstring = result.read()
		data = simplejson.loads(jsonstring)
		return data
		