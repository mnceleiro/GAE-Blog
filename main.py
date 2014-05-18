# -*- coding: utf-8 -*-

import webapp2
import os
import jinja2

from admin import AdminHandler
from entities import Post

from google.appengine.ext import ndb
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
		loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ),
		extensions=[ "jinja2.ext.autoescape" ],
		autoescape=True )

class MainHandler(webapp2.RequestHandler):
	def __init__(self, request=None, response=None):
		self.initialize(request, response)

	def get(self):
		user = users.get_current_user()
		limit = 5
		
		''' Paginación '''
		prev_go = self.request.get('prev_go')
		cursor = ndb.Cursor(urlsafe=self.request.get('cursor',default_value=None))
		
		if (self.request.get('go') == 'newer'):
			query = Post.query().order( Post.date )	# Los posts van por fecha de viejos a recientes [4,3,2,1]
			
			if prev_go == 'older':
				_, next_cursor, _ = query.fetch_page(limit, start_cursor=cursor.reversed())
				query, next_cursor, more = query.fetch_page(limit, start_cursor=next_cursor)
			else:
				query, next_cursor, more = query.fetch_page(limit, start_cursor=cursor.reversed())
				
			query = reversed(query)
			
			next_cursor = next_cursor.reversed()
			
		else:
			query = Post.query().order( -Post.date )	# Los posts van por fecha de recientes a viejos [1,2,3,4]

			if prev_go == 'newer':
				_, next_cursor, _ = query.fetch_page(limit, start_cursor=cursor)
				query, next_cursor, more = query.fetch_page(limit, start_cursor=next_cursor)
			else:
				query, next_cursor, more = query.fetch_page(limit, start_cursor=cursor)
			
		if next_cursor:	
			next_cursor = next_cursor.urlsafe()
			
		values = {
			'posts': query,
			'cursor': str(next_cursor),
			'prev_go': self.request.get('go'),
			'user': user,
			'users': users
	    }
		
		if self.request.get('msg'):
			values['msg'] = self.request.get('msg')
			
		template = JINJA_ENVIRONMENT.get_template( "static/templates/index.html" )
		self.response.write( template.render( values ) );
		
	
	def login(self):
		login_template = JINJA_ENVIRONMENT.get_template('/static/templates/login.html')
		self.response.write(login_template.render())
		
	def about(self):
		values = {
			'user': users.get_current_user(),
			'users': users,
		}

		template = JINJA_ENVIRONMENT.get_template('/static/templates/about.html')
		self.response.write(template.render(values))
		
	def blogpost(self):
		id = self.request.get("id")
		
		post = Post.get_by_id(int(id))
# 		print post
		
		user = users.get_current_user()
		
		values = {
			'post': post,
			'user': user,
			'users': users,
		}
		
		if (str(self.request.get("id")) == str(post.key.id())):
			template = JINJA_ENVIRONMENT.get_template('/static/templates/blogpost.html')
			self.response.write(template.render(values))
		

app = webapp2.WSGIApplication([
    webapp2.Route('/login', handler="main.MainHandler", handler_method='login'),
    webapp2.Route('/about', handler="main.MainHandler", handler_method='about'),
	webapp2.Route('/blogpost', handler="main.MainHandler", handler_method="blogpost"),
	webapp2.Route('/addform', handler="main.AdminHandler", handler_method='addform'),
	webapp2.Route('/add', handler="main.AdminHandler", handler_method='add'),
	webapp2.Route('/header', handler="main.AdminHandler", handler_method='header'),
	webapp2.Route('/logout', handler="main.AdminHandler", handler_method='logout'),
	webapp2.Route('/delete', handler="main.AdminHandler", handler_method='delete'),
	webapp2.Route('/update', handler="main.AdminHandler", handler_method='update'),
    ('/', MainHandler),
    ('/admin', AdminHandler)
    ], debug=True)