from django.shortcuts import HttpResponse, render
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
import math

from OPG_Plac import models

# helpers


def serialize_products(products_qset):

    serialized_products = []
    for product in products_qset:
        serialized_products.append({
            "name": product.name,
            "seo_url": product.seo_url,
            "image": product.product_image,
            "price": product.price,
            "short_desc": product.short_description
        })

    return serialized_products

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

    print(categories_list)

    return render(request, "index.html", {
        "categories": categories_list
    })


def view_about(request):
    return render(request, "components/about/about.html", {})


# render blog overview page -- returns blog categories from db and sends them as a list to template
def view_blog_previews(request):
    category_filter = request.GET.get("filter", "all")

    blog_categories = models.BlogCategory.objects.all().order_by('position_index')

    categories = []  # Sort categories and pack in list
    for category in blog_categories:
        categories.append(category.category)

    return render(request, "components/blog/blog.html", {
        "categories": categories,
        "category_filter": category_filter
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
    total_pages = math.ceil(len(products) / 15)

    # Paginate
    try:
        p = Paginator(products, 15)
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

