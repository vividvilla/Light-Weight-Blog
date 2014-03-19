#!/usr/bin/env python

import webapp2
import re
import random
import string
import hashlib
from google.appengine.api import memcache

SECRET = "PAEQLNoz1j"
SESSION_KEY = "loggedin"

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
pass_re = verify_re = re.compile(r"^.{3,20}$")
email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
	return user_re.match(username)
    
def valid_pass(password):
    return pass_re.match(password)
    
def valid_email(email):
    if len(email) > 0:
        return email_re.match(email)
    return True

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))
        
def make_pw_hash(pw, name=SECRET, salt=""):
    if salt == "":
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)
        
def valid_pw(pw, h, name=SECRET):
    salt = h.split('|')[1]
    if make_pw_hash(pw, name, salt) == h:
        return True
        
def make_id_hash(username):
	h = hashlib.sha256(SECRET+username).hexdigest()
	return "{}|{}".format(username,h)

def verify_id_hash(inhash):
	uname = inhash.split('|')[0]
	if inhash == make_id_hash(uname) :
	    return True
	
class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        memcache.delete(SESSION_KEY)
        self.response.delete_cookie('username')
        self.redirect('/signup')  
            
app = webapp2.WSGIApplication([
    (r'/logout/?', LogoutHandler),
], debug=True)