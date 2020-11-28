from django.contrib import admin

import OPG_Plac.models as models

# Register your models here.

admin.site.register([

    models.User,
    models.BlogArticle,
    models.BlogCategory,
    models.ProductCategory,
    models.ProductSubCategory

])
