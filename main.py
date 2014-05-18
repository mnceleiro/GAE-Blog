# -*- coding: utf-8 -*-

import webapp2
import os
import jinja2

from admin import AdminHandler
from entities import Post

from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor

JINJA_ENVIRONMENT = jinja2.Environment(
		loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ),
		extensions=[ "jinja2.ext.autoescape" ],
		autoescape=True )


def getPosts(cursor, limit):
	if (limit):
		posts, next_cursor, more = Post.query().order( -Post.date ).fetch_page(limit, start_cursor=cursor)
		print posts
	else:
		posts, next_cursor, more = Post.query().order( -Post.date ).fetch()

	return posts, next_cursor, more


def doOlderPagination(request, cursor, limit):
	if (request.get('prev_go') == 'newer'):
		cursor = cursor.reversed()
	
	query = Post.query().order( -Post.date )
	posts, next_cursor, more = query.fetch_page(int(request.get('numEls')), start_cursor=cursor)

	if (request.get('prev_go') == 'newer'):
		posts, next_cursor, more = query.fetch_page(limit, start_cursor=next_cursor)
	
	return posts, next_cursor, more
		
		
def doNewerPagination(request, cursor, limit):
	if (request.get('prev_go') == 'older'):
		cursor = cursor.reversed()
			
	query = Post.query().order( Post.date )
	posts, next_cursor, more = query.fetch_page(int(request.get('numEls')), start_cursor=cursor)

	if (request.get('prev_go') == 'older'):
		posts, next_cursor, more = query.fetch_page(limit, start_cursor=next_cursor)

	return posts[::-1], next_cursor, more

def doPagination(limit, request):
	cursor = Cursor(urlsafe=request.get('cursor', default_value=None))
	
	go = request.get('go')
	
	if (not go):
		posts, next_cursor, more = getPosts(cursor, limit)
		more = False
		
		if not next_cursor:
			return [], "", None
	elif (go == 'older'):
		posts, next_cursor, more = doOlderPagination(request, cursor, limit)
	else:
		posts, next_cursor, more = doNewerPagination(request, cursor, limit)
	
	next_cursor = next_cursor.urlsafe()
	
	return posts, next_cursor, more


class MainHandler(webapp2.RequestHandler):
	def __init__(self, request=None, response=None):
		self.initialize(request, response)


	def get(self):
		if self.request.get('limit'):
			limit = int(self.request.get('limit'))
		else:
			limit = 3 # default limit

		posts, next_cursor, more = doPagination(limit, self.request)
		
		values = {
			'users': users,
			'user': users.get_current_user(),
			'posts': posts,
			'cursor': next_cursor,
			'more': more,	# Comprobar en la plantilla si hay mas elementos para mostrar el boton de paginado corresponndiente
			'prev_go': self.request.get('go'),
			'limit': limit,
			'numEls': len(posts),
			'msg': self.request.get('msg')
		}
		
		template = JINJA_ENVIRONMENT.get_template('/static/templates/index.html')
		self.response.write( template.render(values) )
		
	
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