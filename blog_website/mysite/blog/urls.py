from django.urls import path 
from . import views
from .feeds import LatestPostsFeed



app_name = 'blog'
# A URL pattern is composed of a string pattern, a view, and, optionally, a name that allows you to name the URL project-wide.
urlpatterns = [
    # param of path() => https://docs.djangoproject.com/en/4.1/intro/tutorial01/#write-your-first-view

    path('', 
        views.post_list,
        name='post_list'
        ), # function based listview
    # as_view is the function(class method) which will connect my MyView class with its url.
    # path('',views.PostListView.as_view(), name='post_list'),  # class based post view
    
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
         views.post_detail, 
         name='post_detail'),
    
    path('<int:post_id>/share/',
        views.post_share,
        name='post_share'
        ),
    
    path('<int:post_id>/comment/',
        views.post_comment, 
        name='post_comment'
        ),
    
    path('tag/<slug:tag_slug>/',
        views.post_list, 
        name='post_list_by_tag'
        ),
    path('feed/',
        LatestPostsFeed(),
        name='post_feed',
        ),
***REMOVED***