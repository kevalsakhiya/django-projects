from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    '''Custom manager.'''
    def get_queryset(self):
        '''to get all published post'''
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):
    '''This model describes the blog-post structure'''

    class Status(models.TextChoices):
        '''Provides the choices for the status of our post'''
        # The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name.
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='blog_posts')
    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    # By using auto_now_add, the date will be saved automatically when creating an object.
    created = models.DateTimeField(auto_now_add=True)
    # By using auto_now, the date will be updated automatically when savin an object.
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                choices=Status.choices,
                                default=Status.DRAFT
    )

    objects = models.Manager() #The defaylt Manager
    published = PublishedManager() # Custom manager
    tags = TaggableManager() # Manager given from taggit
    
    # Model Meta is basically the inner class of your model class. Model Meta is basically used to change the behavior 
    # of your model fields like changing order options,verbose_name, and a lot of other options. It’s completely optional to add a Meta class to your model.
    class Meta:
        '''We are adding ordering attribute in meta, to tell django to sort posts by publish field'''
        ordering=['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        '''This is the default Python method to return a string with the human-readable representation of the object.'''
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[
                            self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug
                        ])

class Comment(models.Model):
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='comments',
                            )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'