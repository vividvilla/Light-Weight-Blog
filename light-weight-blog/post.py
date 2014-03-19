#!/usr/bin/env python

import webapp2
import json

from main import Handler
from db import BlogDb
from google.appengine.ext import db

from utils import *

POST_KEY = "posts"

class SignlePostHandler(Handler):
    def render_post(self,title="",content="",date_modified="",date_created=""):
        self.render("singlepost.html", title = title, content = content, date_modified = date_modified, date_created = date_created )
        
    def get(self,post_id):
        sp = memcache.get(post_id)
        if sp is None:
            sp = BlogDb.get_by_id(int(post_id))
            memcache.set(post_id,sp)
        self.render_post(sp.title,sp.content,sp.date_modified,sp.date_published)

class NewPostHandler(Handler):
    def render_front(self,title="",content="",error=""):
        self.render("newpost.html", title = title, content = content, error = error)
        
    def get(self):
        session = memcache.get(SESSION_KEY) 
        if session:
            self.render_front()
        else:
            self.redirect('/signup')
    
    def post(self):
		title = self.request.get("subject")
		content = self.request.get("content")
		if title and content:
			newcontent = BlogDb(title = title, content = content)
			a = newcontent.put()
			post_id = a.id()
			memcache.delete(POST_KEY)
			self.redirect('/blog/{}'.format(post_id))
		else:
			error = "Need both the fields to be filled"
			self.render_front(title,content,error)
			
class MainHandler(Handler):
	def render_home(self):
	    allposts = memcache.get(POST_KEY)
	    if allposts is None:
	        allposts = db.GqlQuery("SELECT * FROM BlogDb ORDER BY date_published DESC LIMIT 10")
	        memcache.set(POST_KEY, allposts)
	    self.render("home.html", allposts = allposts)
	    
	def get(self):
		self.render_home()
			
def post_json(singlepost):
    json_str = {}
    if singlepost:
        json_str["content"] = singlepost.content
        json_str["created"] = singlepost.date_modified.strftime("%d %b %Y %H:%M:%S GMT")
        json_str["last_modified"] = singlepost.date_modified.strftime("%d %b %Y %H:%M:%S GMT")
        json_str["subject"] = singlepost.title
    return json_str

class JsonHandler(Handler):
    def get(self,*args):
        jstr = {"content": "","created": "","last_modified": "","subject":""}
        self.response.headers["Content-Type"] = "application/json"
        if args:
            singlepost = BlogDb.get_by_id(int(args[0]))
            json_str = post_json(singlepost)
            self.response.out.write(json.dumps(json_str))
        else:
            allposts = memcache.get(POST_KEY)
            if allposts is None:
                allposts = db.GqlQuery("SELECT * FROM BlogDb ORDER BY date_published DESC LIMIT 10")
                memcache.set(POST_KEY,allposts)
            jall = []
            for singlepost in allposts:
                json_str = post_json(singlepost)
                jall.append(json_str) 
            self.response.out.write(json.dumps(jall))
            
app = webapp2.WSGIApplication([
    (r'/blog/?', MainHandler),
    (r'/newpost/?',NewPostHandler),
    (r'/blog/(\d+)', SignlePostHandler),
    (r'/blog.json/?', JsonHandler),
    (r'/blog/.json/?', JsonHandler),
    (r'/blog/(\d+).json/?', JsonHandler)
], debug=True)