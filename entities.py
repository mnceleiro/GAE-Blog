from google.appengine.ext import ndb


class Post(ndb.Model):
    name = ndb.StringProperty( required = True)
    description = ndb.StringProperty(required = True)
    author = ndb.StringProperty(required = True)
    date = ndb.DateTimeProperty( auto_now_add = True)
    
class Comment(ndb.Model):
    user = ndb.StringProperty( required = False )
    comment = ndb.StringProperty ( required = True )
