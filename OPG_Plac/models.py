from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


##### User Models ########


# Custom User_Manager, per django documentation
class UserManager(BaseUserManager):
    def create_user(self, email, password, name):
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, name):
        user = self.create_user(email, password, name)

        user.is_staff = True  # Admins are staff
        user.is_admin = True

        user.save(using=self._db)

        return user


# Defined Custom User model, per django documentation
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="email_address", max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Login via email
    REQUIRED_FIELDS = ['name']

    objects = UserManager()  # Assign custom user_manager to a custom_user

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

##### Blog Models ########


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


##### Product Models ########


class ProductBrand(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to="banners")

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    category = models.CharField(max_length=30)
    position_index = models.IntegerField(null=True, blank=True)
    category_img = models.ImageField(null=True, blank=True, upload_to="images")
    on_homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.category


class ProductSubCategory(models.Model):
    parent_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="subcategories")
    subcategory = models.CharField(max_length=30)
    position_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.subcategory} - [{self.parent_category}]"


class ProductAvailability(models.Model):
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return self.status_name


class Product(models.Model):
    name = models.CharField(max_length=67)
    seo_url = models.SlugField(unique=True)
    item_id = models.SlugField(unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    subcategory = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, related_name="products")
    product_image = models.ImageField(blank=True, null=True, upload_to="images/products")
    second_image = models.ImageField(blank=True, null=True, upload_to="images/products")
    third_image = models.ImageField(blank=True, null=True, upload_to="images/products")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    short_description = models.CharField(max_length=75, blank=True)
    description = models.TextField(blank=True, max_length=435)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    availability = models.ForeignKey(ProductAvailability, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name
























