from django.http import JsonResponse
from django.utils.html import strip_tags

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

    if request.GET["filter"] == "all":   # Filter articles by category
        articles = models.BlogArticle.objects.all()
    else:
        category_filter = models.BlogCategory.objects.get(category=request.GET["filter"])
        articles = models.BlogArticle.objects.filter(category=category_filter)

    previews = serialize_previews(articles)

    return JsonResponse(
        {"previews": previews},
        status=200,
        safe=False,
        json_dumps_params={'ensure_ascii': False}
        )

