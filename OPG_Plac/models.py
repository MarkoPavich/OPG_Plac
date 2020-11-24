from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class BlogCategory(models.Model):
    category = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.category


class BlogArticle(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=150)
    title_img = models.URLField(name="title_image")
    content = models.TextField(name="Article_content")
    seo_url = models.SlugField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    seo_keywords = models.CharField(max_length=50)

    def __str__(self):
        return self.title


