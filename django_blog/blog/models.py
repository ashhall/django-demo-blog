from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()  # unrestricted text
    """no parentheses after now because you don't want to 
        execute the function, you are passing it in as a param"""
    date_drafted = models.DateTimeField(default=timezone.now)
    date_published = models.DateTimeField(blank=True, null=True)
    # on_delete => if user is deleted, delete their post too
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_blog_pic.jpg', upload_to='blog_pics')  # upload image to dir: 'blog_pics'
    likes = models.ManyToManyField(User, related_name='like')

    def publish(self):
        self.date_published = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # returns full path as string
        return reverse('post_detail', kwargs={'pk': self.pk})



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['timestamp',]

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Comment by {self.author}'