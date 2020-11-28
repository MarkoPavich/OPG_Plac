from django.shortcuts import HttpResponse, render
from django.core.exceptions import ObjectDoesNotExist

from OPG_Plac import models

# Create your views here.


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


def index(request):
    return render(request, "index.html", {})


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
    products = serialize_products(products)  # Serialize products

    return render(request, "components/products/products.html", {
        "categories": categories_dict,
        "products": products,
        "active_category": category_filter,
        "active_subcategory": subcategory_filter
    })

