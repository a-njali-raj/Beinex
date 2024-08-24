from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to="media/profile-pics/", null=True, blank=True,)
    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag=models.CharField(max_length=50,blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # New image field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)