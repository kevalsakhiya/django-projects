from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


def post_list(request):
    '''Returns all published posts'''
    posts  =Post.published.all()
    return render(request,
                    'blog/post/list.html',
                ***REMOVED***'posts':posts***REMOVED***)

def post_detail(request,id):
    post = get_object_or_404(Post,
                            id=id,
                            status=Post.Status.PUBLISHED
                            )

    return render(request,
                    'blog/post/detail.html',
                ***REMOVED***'post':post***REMOVED***                    
                    )
