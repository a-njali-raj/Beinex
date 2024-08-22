from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(blank=True)
    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # New image field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)