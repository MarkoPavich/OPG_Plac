from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class BlogCategory(models.Model):
    category = models.CharField(max_length=20, unique=True)
    position_index = models.IntegerField(null=True, blank=True)

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


class ProductCategory(models.Model):
    category = models.CharField(max_length=30)
    position_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.category


class ProductSubCategory(models.Model):
    parent_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="subcategories")
    subcategory = models.CharField(max_length=30)
    position_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.subcategory} - [{self.parent_category}]"


class Product(models.Model):
    name = models.CharField(max_length=100)
    seo_url = models.SlugField(unique=True)
    item_id = models.SlugField(unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    subcategory = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, related_name="products")
    product_image = models.URLField()
    second_image = models.URLField(blank=True)
    third_image = models.URLField(blank=True)
    fourth_image = models.URLField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



























