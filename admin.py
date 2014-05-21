# -*- coding: utf-8 -*-

import os

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2

from entities import Post


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ),
    extensions=[ "jinja2.ext.autoescape" ],
    autoescape=True )



class AdminHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        
    def get(self):
        user = users.get_current_user()
        
        if user:
            self.redirect('/?msg=Se ha identificado correctamente.')
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
        
    def add(self):
        user = users.get_current_user()
        
        values = {
                'user': user,
                'users': users, #
        }
        
        template = JINJA_ENVIRONMENT.get_template("/static/templates/addform.html")
        self.response.write (template.render(values))
        
    def post(self):
        self.name = self.request.get('name')
        self.author = str(users.get_current_user())
        
        if (users.is_current_user_admin()):
            post = Post(name = self.name, description = self.request.get('description').encode('utf-8'), author = self.author)
            post.put()
            return self.redirect('/?msg=El post se ha realizado correctamente')
        else:
            return self.redirect('/?msg=No puede escribir posts porque no es administrador del sitio web.')
        
    
    def delete(self):
        toDelete = self.request.get('id')
        
        if (users.is_current_user_admin() and toDelete):
            ndb.Key(Post, int(toDelete)).delete()
            self.redirect('/?msg=El post ha sido borrado correctamente')
        else:
            self.redirect('/?msg="El post no se ha guardado.')
        
        
    def update(self):
        toUpdate = self.request.get('id')
        post = Post.get_by_id(int(toUpdate))
        
        post.description = self.request.get('description')
        post.last_edit_author = str(users.get_current_user())
        
        if post.description and post.last_edit_author and toUpdate:
            post.put()
            self.redirect("/?msg=El post ha sido editado correctamente.")
        else:
            self.redirect('/?msg=El post no ha podido actualizarse.')
    
    def logout(self):
        self.redirect(users.create_logout_url('/'))
            
