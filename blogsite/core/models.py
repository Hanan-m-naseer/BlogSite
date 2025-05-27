from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def str (self):
        return self.user.username
    
class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title