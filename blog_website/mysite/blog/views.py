from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank

class PostListView(ListView):
    ***REMOVED***
    Alternative post list view
    ***REMOVED***
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request,tag_slug=None):
    '''Returns all published posts'''
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag***REMOVED***)

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
                ***REMOVED***'posts':posts,
                    'tag':tag,
                ***REMOVED***
                    )

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

    # List of similar post
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4***REMOVED***
    return render(request,
                    'blog/post/detail.html',
                ***REMOVED***'post':post,
                    'comments': comments,
                    'form': form,
                    'similar_posts':similar_posts,
            ***REMOVED***
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

def post_search(request):
    form = SearchForm()
    query = None
    results = [***REMOVED***

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query'***REMOVED***
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
    results = Post.published.annotate(
                                search=search_vector,rank=SearchRank(search_vector, search_query)
                                ).filter(rank__gte=0.3).order_by('-rank')
    
    return render(request,
                'blog/post/search.html',
            ***REMOVED***'form': form,
                'query': query,
                'results': results***REMOVED***,
                )