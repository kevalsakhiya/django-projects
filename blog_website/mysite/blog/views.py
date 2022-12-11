from django.shortcuts import render, get_object_or_404
from .models import Post
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    '''Returns all published posts'''
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1) # .get() returns 1 if there is no page given
   
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)

    return render(request,
                    'blog/post/list.html',
                ***REMOVED***'posts':posts***REMOVED***)

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day
                            )

    return render(request,
                    'blog/post/detail.html',
                ***REMOVED***'post':post***REMOVED***                    
                    )
