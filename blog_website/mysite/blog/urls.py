from django.urls import path
from . import views

app_name = 'blog'
# A URL pattern is composed of a string pattern, a view, and, optionally, a name that allows you to name the URL project-wide.
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail')
***REMOVED***