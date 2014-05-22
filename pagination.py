# -*- coding: utf-8 -*-

''' Método principal '''

from google.appengine.datastore.datastore_query import Cursor

from entities import Post


def do_pagination(limit, request, condition=None):
    cursor = Cursor(urlsafe=request.get('cursor', default_value=None))
    go = request.get('go')

    if (condition):
        pass
    else:
        pass
    
    if (not go):
        posts, next_cursor, more = _get_posts(cursor, limit, condition)
        
        if not next_cursor:
            return [], "", None
#         if not more:
#             more = False
        
    elif (go == 'older'):
        posts, next_cursor, more = _do_older_pagination(request, cursor, limit)
    else:
        posts, next_cursor, more = _do_newer_pagination(request, cursor, limit)
    
    next_cursor = next_cursor.urlsafe()
    
    return posts, next_cursor, more


''' Métodos "privados" '''
def _get_posts(cursor, limit, condition=None):
    if condition:
        posts, next_cursor, more = Post.query(eval(condition)).order( -Post.date ).fetch_page(limit, start_cursor=cursor)
    else:
        posts, next_cursor, more = Post.query().order( -Post.date ).fetch_page(limit, start_cursor=cursor)
    
    return posts, next_cursor, more

def _get_posts_with_condition(cursor, limit, condition):
        return Post.query(condition).order( -Post.date ).fetch_page(limit, start_cursor=cursor)
    
def _do_older_pagination(request, cursor, limit):
    if (request.get('prev_go') == 'newer'):
        cursor = cursor.reversed()
    
    query = Post.query().order( -Post.date )
    posts, next_cursor, more = query.fetch_page(int(request.get('numEls')), start_cursor=cursor)

    if (request.get('prev_go') == 'newer'):
        posts, next_cursor, more = query.fetch_page(limit, start_cursor=next_cursor)
    
    return posts, next_cursor, more
        
        
def _do_newer_pagination(request, cursor, limit):
    if (request.get('prev_go') == 'older'):
        cursor = cursor.reversed()
            
    query = Post.query().order( Post.date )
    posts, next_cursor, more = query.fetch_page(int(request.get('numEls')), start_cursor=cursor)

    if (request.get('prev_go') == 'older'):
        posts, next_cursor, more = query.fetch_page(limit, start_cursor=next_cursor)

    ''' posts es devuelto como una lista inversa '''
    return posts[::-1], next_cursor, more 


