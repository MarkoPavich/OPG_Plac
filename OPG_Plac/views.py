from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
import math
import json

from OPG_Plac import models


# helpers


def serialize_user_info(extended_user):
    user_info = {
        "first_name": extended_user.user.first_name,
        "last_name": extended_user.user.last_name,
        "address": extended_user.address,
        "place": extended_user.place,
        "post_code": extended_user.post_code,
        "phone": extended_user.phone,
        "same_delivery": extended_user.same_delivery,
        "need_R1": extended_user.need_R1
    }

    if not extended_user.same_delivery:
        delivery_info = {
            "delivery_first_name": extended_user.delivery_first_name,
            "delivery_last_name": extended_user.delivery_last_name,
            "delivery_address": extended_user.delivery_address,
            "delivery_place": extended_user.delivery_place,
            "delivery_post_code": extended_user.delivery_post_code,
            "delivery_phone": extended_user.delivery_phone
        }

        user_info.update(delivery_info)

    if extended_user.need_R1:
        company_info = {
            "company_name": extended_user.company_name,
            "company_address": extended_user.company_address,
            "company_post_code": extended_user.company_post_code,
            "OIB": extended_user.OIB
        }

        user_info.update(company_info)

    print(user_info)
    return user_info


def serialize_previews(queryset):
    serialized_previews = []

    for article in queryset:
        serialized_previews.append({
            "img": article.title_image,
            "title": article.title,
            "preview": strip_tags(article.Article_content)[0:223],
            "seo_url": article.seo_url
        })

    return serialized_previews


def serialize_products(products_qset):

    serialized_products = []
    for product in products_qset:

        try:
            image = product.product_image.url
        except ValueError:
            image = None

        serialized_products.append({
            "name": product.name,
            "seo_url": product.seo_url,
            "image": image,
            "price": product.price,
            "short_desc": product.short_description,
            "item_id": product.item_id
        })

    return serialized_products


def serialize_cart(cart_qset):

    serialized_cart = []
    for item in cart_qset:
        if item.quantity != 0:
            serialized_cart.append({
                "name": item.product.name,
                "img": item.product.product_image,
                "seo_url": item.product.seo_url,
                "price": item.product.price,
                "quantity": item.quantity,
                "sum": item.product.price * item.quantity,
                "item_id": item.product.item_id
            })
        else:
            item.delete()  # Delete item if quantity is 0

    return serialized_cart

# views


def index(request):

    categories_qset = models.ProductCategory.objects.filter(on_homepage=True).order_by("position_index")

    # Get homepage_square categories
    categories_list = []
    for category in categories_qset:
        categories_list.append({
            "name": category.category,
            "image": category.category_img
        })

    return render(request, "index.html", {
        "categories": categories_list
    })


def view_about(request):
    return render(request, "components/about/about.html", {})


# render blog overview page -- returns blog categories from db and sends them as a list to template
def view_blog_previews(request):

    category_filter = request.GET.get("category", "all")
    page_num = int(request.GET.get("page", 1))

    blog_categories = models.BlogCategory.objects.all().order_by('position_index')

    categories = []  # Sort categories and pack in list
    for category in blog_categories:
        categories.append(category.category)

    if category_filter == "all":   # Filter articles by category
        qset = models.BlogArticle.objects.all()

    else:
        category_obj = models.BlogCategory.objects.get(category=category_filter)
        qset = models.BlogArticle.objects.filter(category=category_obj)

    total_pages = math.ceil(len(qset) / 8)

    try:
        p = Paginator(qset, 8,)
        articles = p.page(page_num)
    except EmptyPage:
        articles = []

    previews = serialize_previews(articles)
    print(category_filter)

    return render(request, "components/blog/blog.html", {
        "categories": categories,
        "category_filter": category_filter,
        "article_previews": previews,
        "total_pages": total_pages,
        "current_page": page_num
    })


def view_blog_article(request):

    seo_url = request.GET["article"]

    try:
        article = models.BlogArticle.objects.get(seo_url=seo_url)
    except ObjectDoesNotExist:
        return render(request, "components/utility/error.html", {
            "error": "Not Found",
            "status": 404,
            "message": "Maybe try again or check spelling ?"
        })

    author = article.author.username
    category = article.category
    title = article.title
    content = article.Article_content
    keywords = article.seo_keywords
    timestamp = article.timestamp
    img = article.title_image
    seo_url = article.seo_url

    return render(request, 'components/blog/view_article/view_article.html', {
        "author": author,
        "category": category,
        "title": title,
        "content": content,
        "keywords": keywords,
        "timestamp": timestamp,
        "img": img,
        "seo_url": seo_url
    })


def view_proizvodi(request):
    results_per_page = 12  # Controls the number of products per pagination page

    category_filter = request.GET.get("category", None)
    subcategory_filter = request.GET.get("subcategory", None)

    page_num = request.GET.get("page", 1)

    category_qset = models.ProductCategory.objects.all().order_by("position_index")  # Fetch category and subcategory qsets
    subcategory_qset = models.ProductSubCategory.objects.all().order_by("position_index")

    categories_dict = {}  # Build a dict with categories and their subcategories
    for category in category_qset:  # Pass to view for categories_menu construction
        subcategories = []

        for subcategory in subcategory_qset:
            if subcategory.parent_category == category:
                subcategories.append(subcategory.subcategory)
        categories_dict[category.category] = subcategories

    # Get products_qset
    if category_filter is None:
        products = models.Product.objects.all()
        subcategory_filter = None  # ensure no active subfilter if main_category filter is None

    else:
        category_obj = models.ProductCategory.objects.get(category=category_filter)

        if subcategory_filter is not None:
            subcategory_obj = models.ProductSubCategory.objects.get(subcategory=subcategory_filter)

            products = models.Product.objects.filter(category=category_obj, subcategory=subcategory_obj)

        else:
            products = models.Product.objects.filter(category=category_obj)

    # Calculate total pages
    total_pages = math.ceil(len(products) / results_per_page)

    # Paginate
    try:
        p = Paginator(products, results_per_page)
        products_page = p.page(page_num)
    except EmptyPage:
        products_page = []

    # Serialize
    products_page = serialize_products(products_page)

    return render(request, "components/products/products.html", {
        "categories": categories_dict,
        "products": products_page,
        "active_category": category_filter,
        "active_subcategory": subcategory_filter,
        "total_pages": total_pages,
        "current_page": page_num
    })


def view_proizvod_artikl(request, product_url):

    try:
        product_obj = models.Product.objects.get(seo_url=product_url)
    except ObjectDoesNotExist:
        return render(request, "components/utility/error.html", {
            "error": "Not Found",
            "status": 404,
            "message": "Maybe try again or check spelling ?"
        })

    try:
        product_img = product_obj.product_image.url
    except ValueError:
        product_img = None

    product = {
        "product_name": product_obj.name,
        "item_id": product_obj.item_id,
        "product_img": product_img,
        "alt_img1": product_obj.second_image,
        "alt_img2": product_obj.third_image,
        "price": product_obj.price,
        "short_description": product_obj.short_description,
        "brand": product_obj.brand.name,
        "banner_img": product_obj.brand.img,
        "availability": product_obj.availability.status_name,
        "category": product_obj.category,
        "subcategory": product_obj.subcategory.subcategory,
        "description": product_obj.description
    }

    return render(request, "components/products/product_view/view_artikl.html", product)


def view_signin(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        return render(request, "components/signin/signin.html", {})


# Logout path
def view_logout(request):
    logout(request)
    return redirect("/")


@login_required(login_url="/prijava")
def view_cart(request):

    user = models.User.objects.get(email=request.user)
    cart = user.cart.all()

    cart_count = sum([item.quantity for item in cart])

    cart = serialize_cart(cart)

    total = float(sum([item["sum"] for item in cart]))
    base_sum = round(total/1.25, 2)
    vat = round(total - base_sum)
    shipping_cost = 20
    total_sum = total + shipping_cost

    return render(request, "components/cart/cart.html", {
        "cart": cart,
        "total": total_sum,
        "base_sum": base_sum,
        "vat": vat,
        "shipping_cost": shipping_cost,
        "cart_count": cart_count
    })


@login_required(login_url="/prijava")
def view_delivery(request):
    user = models.User.objects.get(email=request.user)

    try:
        user_info = serialize_user_info(user.extendeduser)
    except ObjectDoesNotExist:
        user_info = {
            "first_name": user.first_name,
            "last_name": user.last_name
        }

    return render(request, "components/cart/delivery.html", user_info)


@login_required(login_url="/prijava")
def view_checkout(request):

    user = models.User.objects.get(email=request.user)
    cart = user.cart.all()

    if len(cart) == 0:
        return redirect("/košarica")

    cart = serialize_cart(user.cart.all())

    try:
        order = user.orders.get(status=None)
    except ObjectDoesNotExist:
        return redirect("/košarica")

    total = float(sum([item["sum"] for item in cart]))
    base_sum = round(total/1.25, 2)
    vat = round(total - base_sum)
    shipping_cost = 20
    total_sum = total + shipping_cost

    payopts_qset = models.PaymentOption.objects.all()
    payment_options = []
    for option in payopts_qset:
        payment_options.append({
            "descriptive_name": option.descriptive_name,
            "reference": option.reference,
            "tooltip": option.tooltip
        })

    context = {
        "cart": cart,
        "total": total_sum,
        "base_sum": base_sum,
        "vat": vat,
        "shipping_cost": shipping_cost,
        "notice": order.notice,
        "payment_options": payment_options
    }

    user_info = {
        "first_name": order.first_name,
        "last_name": order.last_name,
        "address": order.address,
        "place": order.place,
        "post_code": order.post_code,
        "phone": order.phone
    }
    
    context.update(user_info)

    delivery_info = {
        "delivery_first_name": order.delivery_first_name if not order.same_delivery else order.first_name,
        "delivery_last_name": order.delivery_last_name if not order.same_delivery else order.last_name,
        "delivery_address": order.delivery_address if not order.same_delivery else order.address,
        "delivery_place": order.delivery_place if not order.same_delivery else order.place,
        "delivery_post_code": order.delivery_post_code if not order.same_delivery else order.post_code,
        "delivery_phone": order.delivery_phone if not order.same_delivery else order.phone
    }

    context.update(delivery_info)

    company_info = {
        "need_R1": order.need_R1,
        "company_name": order.company_name,
        "company_address": order.company_address,
        "company_post_code": order.company_post_code,
        "OIB": order.OIB
    }

    context.update(delivery_info)

    return render(request, "components/cart/checkout.html", context)
















