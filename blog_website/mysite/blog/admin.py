from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''We are telling the Django administration site that the model is registered in the site using a custom
    class that inherits from ModelAdmin. In this class, we can include information about how to display
    the model on the site and how to interact with it.'''

    # The list_display attribute allows you to set the fields of your model that you want to display on the administration object list page.
    list_display =  ['title','slug','author','publish','status']
    # list_filter attribute defines the ways of filtering the results by the fields included in it.
    list_filter = ['status', 'created', 'publish', 'author']
    # search_bar appears on the page in which we cans earch the posts by searchable fields.
    search_fields = ['title','body']
    # populates slug field based on title
    prepopulated_fields = {'slug':('title',)}
    # this provides a lookup-widget on screen and fill it with the id of the author
    raw_id_fields = ['author']
    # adds date based drilled down navigation on the page
    date_hierarchy = 'publish'
    # With this we cann order the posts by given field name in ordering
    ordering = ['status','publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']