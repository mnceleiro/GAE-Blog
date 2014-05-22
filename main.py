# -*- coding: utf-8 -*-

import os

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2

from admin import AdminHandler
from entities import Post
from entities import Comment

import pagination


JINJA_ENVIRONMENT = jinja2.Environment(
		loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ),
		extensions=[ "jinja2.ext.autoescape" ],
		autoescape=True )


class MainHandler(webapp2.RequestHandler):
	def __init__(self, request=None, response=None):
		self.initialize(request, response)

	
	def get(self):
		if self.request.get('limit'):
			limit = int(self.request.get('limit'))
		else:
			limit = 3 # default limit

		posts, next_cursor, more = pagination.do_pagination(limit, self.request)
		
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
		
		
	def about(self):
		values = {
			'user': users.get_current_user(),
			'users': users,
		}

		template = JINJA_ENVIRONMENT.get_template('/static/templates/about.html')
		self.response.write(template.render(values))
		
		
	def blogpost(self):
		id_post = self.request.get("id")
		
		post = Post.get_by_id(int(id_post))
		user = users.get_current_user()
		comments = Comment.query(Comment.post_id == ndb.Key(Comment, id_post)).order(-Comment.date).fetch()

		values = {
			'post': post,
			'user': user, #
			'users': users,
			'comments': comments,
		}
		
		if (str(id_post) == str(post.key.id())):
			template = JINJA_ENVIRONMENT.get_template('/static/templates/blogpost.html')
			self.response.write(template.render(values))
		
			
	def comment(self):
		post_id = self.request.get('id')
		comm = self.request.get('comment')
		comm_author = str(users.get_current_user())
		
		if comm_author and comm and post_id:
			commentToAdd = Comment(post_id = ndb.Key(Comment, post_id), author = comm_author, comment = comm)
			commentToAdd.put()
		else:
			self.redirect('/?msg="El comentario no se ha podido insertado.')


app = webapp2.WSGIApplication([
    webapp2.Route('/login', handler="main.MainHandler", handler_method='login'),
    webapp2.Route('/about', handler="main.MainHandler", handler_method='about'),
	webapp2.Route('/blogpost', handler="main.MainHandler", handler_method="blogpost"),
	webapp2.Route('/addform', handler="main.AdminHandler", handler_method='add'),
	webapp2.Route('/logout', handler="main.AdminHandler", handler_method='logout'),
	webapp2.Route('/delete', handler="main.AdminHandler", handler_method='delete'),
	webapp2.Route('/update', handler="main.AdminHandler", handler_method='update'),
	webapp2.Route('/comment', handler="main.MainHandler", handler_method='comment'),
    ('/', MainHandler),
    ('/admin', AdminHandler)
    ], debug=True)