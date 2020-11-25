import math
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.core.paginator import Paginator, EmptyPage

from OPG_Plac import models


def get_blog_previews(request):

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

    page_num = int(request.GET["page"])

    if request.GET["filter"] == "all":   # Filter articles by category
        qset = models.BlogArticle.objects.all()

        total_pages = math.ceil(len(qset)/8)

    else:
        category_filter = models.BlogCategory.objects.get(category=request.GET["filter"])
        qset = models.BlogArticle.objects.filter(category=category_filter)

        total_pages = math.ceil(len(qset) / 8)

    try:
        p = Paginator(qset, 8,)
        articles = p.page(page_num)
    except EmptyPage:
        articles = []

    previews = serialize_previews(articles)

    return JsonResponse(
        {
            "previews": previews,
            "total_pages": total_pages,
        },
        status=200,
        safe=False,
        json_dumps_params={'ensure_ascii': False}
        )


def make_unique():
    qset = models.BlogArticle.objects.all()

    i = 0
    for article in qset:
        article.seo_url = f"{article.seo_url }-{i}"
        article.save()
        i = i+1
