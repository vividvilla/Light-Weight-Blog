Light-Weight-Blog
=================

Simple Python(webapp2) based blogging engine hosted on Google Appengine.

What it does ?
--------------

1. Inbuilt user authetication and session management(memcache)
2. Register users can submit blog post
3. Fron page shows last 10 blog posts
4. Minimised DB queries using memcache
5. JSON API Interface (currently for blog posts and home page only)

Functional DEMO - http://light-weight-blog.appspot.com/

Dependencies
------------

1. Google Appengine Datastore
2. Jinja 2

Will it be improved ?
---------------------
Yes, I hope so. Please be free to fork it.

Theses are some features to be implemented

1. Markdown editor
2. Tagging and Categorization of blog posts
3. User profiles with user associated contents
4. Ability to edit blog posts
5. Ability to change user passwords
6. Content revisions
7. API for user authentications and creating posts
8. Support for other databases
