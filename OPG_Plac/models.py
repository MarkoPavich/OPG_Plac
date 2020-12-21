from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


##### User Models ########


# Custom User_Manager, per django documentation
class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name="", last_name=""):
        if email is None:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must provide a password")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name="", last_name=""):
        user = self.create_user(email, password, first_name, last_name)

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
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Login via email
    REQUIRED_FIELDS = ['first_name', "last_name"]

    objects = UserManager()  # Assign custom user_manager to a custom_user

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    address = models.CharField(max_length=200)
    place = models.CharField(max_length=100)
    post_code = models.CharField(max_length=5)
    phone = models.CharField(max_length=20)

    delivery_first_name = models.CharField(max_length=100, blank=True)
    delivery_last_name = models.CharField(max_length=150, blank=True)
    delivery_address = models.CharField(max_length=200, blank=True)
    delivery_place = models.CharField(max_length=100, blank=True)
    delivery_post_code = models.CharField(max_length=5, blank=True)
    delivery_phone = models.CharField(max_length=20, blank=True)

    company_name = models.CharField(max_length=200, blank=True)
    company_address = models.CharField(max_length=200, blank=True)
    company_post_code = models.CharField(max_length=5, blank=True)
    OIB = models.CharField(max_length=11, blank=True)

    same_delivery = models.BooleanField(default=True)
    need_R1 = models.BooleanField(default=False)


##### Blog Models ########


class BlogCategory(models.Model):
    category = models.CharField(max_length=20, unique=True)
    position_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Blog categories"


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

    class Meta:
        verbose_name_plural = "Product categories"


class ProductSubCategory(models.Model):
    parent_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="subcategories")
    subcategory = models.CharField(max_length=30)
    position_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.subcategory} - [{self.parent_category}]"

    class Meta:
        verbose_name_plural = "Product subcategories"


class ProductAvailability(models.Model):
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name_plural = "Product availabilities"


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


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts")
    quantity = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="When added")


####  Ordering system models #####


class PaymentOption(models.Model):
    option = models.CharField(max_length=100)

    def __str__(self):
        return self.option


class OrderStatus(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)

    address = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    post_code = models.CharField(max_length=5)
    phone = models.CharField(max_length=20)

    same_delivery = models.BooleanField(default=True)
    delivery_first_name = models.CharField(max_length=100, blank=True)
    delivery_last_name = models.CharField(max_length=150, blank=True)
    delivery_address = models.CharField(max_length=200, blank=True)
    delivery_place = models.CharField(max_length=100, blank=True)
    delivery_post_code = models.CharField(max_length=5, blank=True)
    delivery_phone = models.CharField(max_length=20, blank=True)

    need_R1 = models.BooleanField(default=False)
    company_name = models.CharField(max_length=200, blank=True)
    company_address = models.CharField(max_length=200, blank=True)
    company_post_code = models.CharField(max_length=5, blank=True)
    OIB = models.CharField(max_length=11, blank=True)

    notice = models.CharField(max_length=200, blank=True)

    paymentOption = models.ForeignKey(PaymentOption, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)


class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    status = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="product", null=True)
    quantity = models.PositiveSmallIntegerField()

    item_name = models.CharField(max_length=67, null=True)
    item_seo_url = models.SlugField(null=True)
    item_id = models.SlugField(null=True)
    item_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)


    def archive_product(self):
        self.item_name = self.product.name
        self.item_seo_url = self.product.seo_url
        self.item_id = self.product.item_id
        self.item_price = self.product.price


















