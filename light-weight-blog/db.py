#!/usr/bin/env python

from google.appengine.ext import db

class BlogDb(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	date_modified = db.DateTimeProperty(auto_now = True)
	date_published = db.DateTimeProperty(auto_now_add = True)
	
class UserDb(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()