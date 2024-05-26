from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', blank=True)  # Adjust upload path as needed

    def __str__(self):
        return f"{self.title} by {self.author}"  # Using f-strings (Python 3.6+)

    def get_absolute_url(self):
        return reverse('home')



