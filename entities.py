from google.appengine.ext import ndb


# class User(ndb.Model):
#     name = ndb.StringProperty( required = True)

class Post(ndb.Model):
    name = ndb.StringProperty( required = True)
    description = ndb.TextProperty(required = True)
    author = ndb.StringProperty(required = True)
    date = ndb.DateTimeProperty( auto_now_add = True)
    last_edit_author = ndb.StringProperty( required = False)
    
class Comment(ndb.Model):
    post_id = ndb.KeyProperty( required = True )
    author = ndb.StringProperty( required = True )
    comment = ndb.TextProperty ( required = True )
    date = ndb.DateTimeProperty( auto_now_add = True)
    
