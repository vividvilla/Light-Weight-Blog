#!/usr/bin/env python

import webapp2

from main import Handler
from db import UserDb
from utils import *
from google.appengine.ext import db

USER_KEY = "userkey"

def user_exists(username):
	user = memcache.get(USER_KEY)
	if user is None:
	    user = db.GqlQuery("SELECT * FROM UserDb")
	    memcache.set(USER_KEY,user)
	if user.get():
	    for singleuser in user:
	        if username == singleuser.username:
	            return singleuser
    
def valid_login(username, password):
    singleuser = user_exists(username)
    if singleuser:
        if valid_pw(password,singleuser.password):
            return True
          
class SignupHandler(Handler):    
    def render_signup(self, username="", email="", username_error="", password_error="", verify_error="", email_error=""):
        self.render("signup.html", username=username, email=email, username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error)
        
    def get(self):
        session = memcache.get(SESSION_KEY)
        if session is None:
            self.render_signup()
        else:  
            self.redirect('/welcome')
        
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        username_error,password_error,verify_error,email_error = [""]*4
        isvalid = True
        
        if not valid_username(username):
            isvalid = False
            username_error = "Not a valid username"

        if user_exists(username):
            isvalid = False
            username_error = "Username already exists"
            
        if not valid_pass(password):
            isvalid = False
            password_error = "Not a valid password"
        else:
            if not password == verify:
                isvalid = False
                verify_error = "Passwords doensn't match"
                
        if not valid_email(email):
            isvalid = False
            email_error = "Invalid email ID"
            
        if isvalid:
            newuser = UserDb(username = username,password = make_pw_hash(password), email = email)
            newuser.put()
            self.response.headers.add_header('Set-Cookie', 'username={}; Path=/'.format(make_id_hash(newuser.username)))
            memcache.set(SESSION_KEY, username)
            memcache.delete(USER_KEY)
            self.redirect('/welcome')
        else:
            self.render_signup(username,email,username_error,password_error,verify_error,email_error)
    
                    
class LoginHandler(Handler):
    def render_login(self, loginerror=""):
        self.render("login.html", loginerror=loginerror)
        
    def get(self):
        session = memcache.get(SESSION_KEY)
        if session is None:
            self.render_login()
        else:
            self.redirect('/welcome')
        
    def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		valid_user,loginerror = True,"Invalid Login"
	
		if not valid_username(username):
			valid_user = False
		
		if not valid_pass(password):
			valid_user = False
	
		if not valid_user or not valid_login(username,password):
			self.render_login(loginerror)
		else:        
			self.response.headers.add_header('Set-Cookie', 'username={}; Path=/'.format(make_id_hash(username)))
			memcache.set(SESSION_KEY, username)
			self.redirect('/welcome')
        
app = webapp2.WSGIApplication([
    (r'/signup/?', SignupHandler),
    (r'/login/?', LoginHandler),
], debug=True)