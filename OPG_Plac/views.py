from django.shortcuts import render
from django.shortcuts import HttpResponse, render

from OPG_Plac import models

# Create your views here.


def index(request):
    return render(request, "index.html", {})


def render_about(request):
    return render(request, "components/about/about.html", {})


def render_blog(request):
    return render(request, "components/blog/blog.html", {})


def view_blog_item(request):

    article = models.BlogArticle.objects.all()[1]

    author = article.author.username
    category = article.category.category
    title = article.title
    content = article.Article_content
    keywords = article.seo_keywords
    timestamp = article.timestamp
    img = article.title_image

    return render(request, 'components/blog/view_article/view_article.html', {
        "author": author,
        "category": category,
        "title": title,
        "content": content,
        "keywords": keywords,
        "timestamp": timestamp,
        "img": img
    })
