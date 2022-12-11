from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST



class PostListView(ListView):
    ***REMOVED***
    Alternative post list view
    ***REMOVED***
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

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
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    return render(request,
                    'blog/post/detail.html',
                ***REMOVED***'post':post,
                    'comments': comments,
                    'form': form***REMOVED***,             
                    )

def post_share(request, post_id):
    # retrive posts by id
    post = get_object_or_404(Post,
                            id=post_id,
                            status=Post.Status.PUBLISHED
                            )
    sent = False
    
    if request.method=='POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name'***REMOVED******REMOVED*** recommends  you read {post.title***REMOVED***"
            message = f"Read {post.title***REMOVED*** at {post_url***REMOVED***\n\n {cd['name'***REMOVED******REMOVED***\'s comments: {cd['comments'***REMOVED******REMOVED***"

            send_mail(subject,message,'olalajulala@gmail.com',[cd['to'***REMOVED******REMOVED***)
            sent = True
    else:
        form = EmailPostForm()

    return render(request,
                'blog/post/share.html',
            ***REMOVED***'post':post,
                'form':form,
                'sent':sent***REMOVED***
                )

@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post,
                            id=post_id,
                            status=Post.Status.PUBLISHED
                            )
    comment = None
    # A comment was created
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()

    return render(request, 
                'blog/post/comment.html',
            ***REMOVED***'post': post,
                'form': form,
                'comment': comment***REMOVED***
                )