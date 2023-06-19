from django.contrib.auth.models import User
from django.db import models

PRIVACY_CHOICES = [
    ('public', 'Public'),
    ('private', 'Private'),
]


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    brief_text = models.CharField(max_length=200,default='brief description')
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    # image = models.ImageField(upload_to='blog_images/')
    def __str__(self):
        return self.title

class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
