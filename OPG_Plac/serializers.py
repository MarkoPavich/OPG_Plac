from django.utils.html import strip_tags


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


# blog previews
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
