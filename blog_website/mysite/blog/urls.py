from django.urls import path 
from . import views

app_name = 'blog'
# A URL pattern is composed of a string pattern, a view, and, optionally, a name that allows you to name the URL project-wide.
urlpatterns = [
    # param of path() => https://docs.djangoproject.com/en/4.1/intro/tutorial01/#write-your-first-view
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
         views.post_detail, 
         name='post_detail')
***REMOVED***