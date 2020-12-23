"""capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from OPG_Plac.views import *
from OPG_Plac import APIs

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Render pipeline

    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('about', view_about, name="about"),
    path('blog/', view_blog_previews, name="blog"),
    path('blog/filter', view_blog_previews, name="blog"),
    path('blog/viewitem', view_blog_article, name="blogitem"),
    path('proizvodi/', view_proizvodi, name="proizvodi"),
    path('proizvodi/filter', view_proizvodi, name="proizvodi"),
    path('proizvodi/viewitem/<slug:product_url>', view_proizvod_artikl, name="proizvod_artikl"),
    path('prijava', view_signin, name="signin"),
    path('odjava', view_logout),
    path("košarica", view_cart),
    path("dostava", view_delivery, name="dostava"),
    path("checkout", view_checkout, name="checkout"),
    path("Confirmation", view_order_confirmation, name="confirmation"),

    # API pipeline

    path('user_registration', APIs.create_user),
    path('login', APIs.login_user),
    path('add_to_cart', APIs.add_to_cart),
    path('pull_cart_count', APIs.get_cart_count),
    path('remove_item_from_cart', APIs.remove_item_from_cart),
    path('update_cart_item_quantity', APIs.update_cart_item_quantity),
    path('submit_delivery_data', APIs.store_delivery_data),
    path("submit_confirmation", APIs.create_order)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
