from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from OPG_Plac import models
import json

import time


def create_user(request):
    # Confirm correct req method
    if request.method != "POST":
        return JsonResponse({
            "message": f"Expected POST request, got '{request.method}'"
        }, status=400)

    # Decode JSON
    json_data = json.loads(request.body)

    # Create User obj
    try:
        # Validate passwords match
        if json_data["password"] != json_data["confirm_password"]:
            return JsonResponse({
                "message": "Passwords don't match",
                "error": "not_matching_passwords"
            }, status=400)

        else:
            user = models.User.objects.create_user(
                first_name=json_data["first_name"],
                last_name=json_data["last_name"],
                email=json_data["email"],
                password=json_data["password"]
            )

    except KeyError:  # Catch no input data
        return JsonResponse({
            "message": "Bad input data"
        }, status=400)

    except IntegrityError:  # Catch email already exists
        return JsonResponse({
            "message": "Email already exists",
            "error": "mail_already_exists"
        }, status=400)

    user = authenticate(request, email=user.email, password=json_data["password"])
    login(request, user)

    return JsonResponse({  # If all checks out, send OK
        "message": "User created, and logged in"
        }, status=200)


def login_user(request):
    if request.method != "POST":
        return JsonResponse({
            "message": f"Expected POST request, got '{request.method}'",
            "error": "bad_request_method"
        }, status=400)

    json_data = json.loads(request.body)

    try:
        email = json_data["email"]
        password = json_data["password"]
    except KeyError:
        return JsonResponse({
            "message": "Bad input data",
            "error": "bad_data_format"
        }, status=400)

    user = authenticate(request, username=email, password=password)

    if user is None:
        return JsonResponse({
            "message": "Email or password invalid",
            "error": "invalid_credentials"
        }, status=401)

    else:
        login(request, user)
        return JsonResponse({
            "message": "Credentials accepted, user signed in"
        }, status=200)


def add_to_cart(request):
    if request.method != "POST":
        return JsonResponse({
            "message": f"Expected POST request, got '{request.method}'",
            "error": "bad_request_method"
        }, status=400)

    try:
        json_data = json.loads(request.body)

        item_id = json_data["item_id"]
        quantity = int(json_data["quantity"])
    except KeyError:
        return JsonResponse({"message": "bad request format"}, status=400)

    if quantity == 0:
        return JsonResponse({"message": "Bad request, cannot add 0 quantity to cart"}, status=400)

    try:
        user = models.User.objects.get(email=request.user)
        product = models.Product.objects.get(item_id=item_id)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Item (likely) or User (unlikely) does not exist"}, status=404)

    cart = user.cart.all()

    try:
        item_in_cart = cart.get(product=product)
        item_in_cart.quantity = item_in_cart.quantity + quantity
        item_in_cart.save()
    except ObjectDoesNotExist:
        cart_item = models.Cart(user=user, product=product, quantity=quantity)
        cart_item.save()

    items_in_cart = 0

    for item in cart:
        items_in_cart = items_in_cart + item.quantity

    return JsonResponse({
        "message": "Item added",
        "items_in_cart": items_in_cart
    }, status=200)


def get_cart_count(request):
    if request.method != "GET":
        return JsonResponse({"message": f"Expected GET request, got '{request.method}'"}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"message": "User not authenticated"}, status=400)

    try:
        user = models.User.objects.get(email=request.user)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "User not found, most likely bad request"}, status=400)

    cart = user.cart.all()

    items_in_cart = 0
    for item in cart:
        items_in_cart = items_in_cart + item.quantity

    return JsonResponse({"in_cart": items_in_cart}, status=200)


def remove_item_from_cart(request):
    if request.method != "DELETE" or not request.user.is_authenticated:
        return JsonResponse({"message": "bad_request_method"}, status=400)

    json_data = json.loads(request.body)

    try:
        user = models.User.objects.get(email=request.user)
        item = models.Product.objects.get(item_id=json_data["item_id"])
    except ObjectDoesNotExist:
        return JsonResponse({
            "message": "User does not exist, most likely bad request"
        }, status=400)
    except KeyError:
        return JsonResponse({
            "message": "Item does not exist, most likely bad request"
            }, status=400)

    cart_item = user.cart.get(product=item)
    cart_item.delete()

    return JsonResponse({"message": "Item removed from cart"}, status=200)


def update_cart_item_quantity(request):
    if request.method != "PUT" or not request.user.is_authenticated:
        return JsonResponse({"message": "bad_request_method"}, status=400)

    json_data = json.loads(request.body)

    try:
        user = models.User.objects.get(email=request.user)
        item = models.Product.objects.get(item_id=json_data["item_id"])
        cart_item = user.cart.get(product=item)
        quantity = int(json_data["quantity"])
    except ObjectDoesNotExist:
        return JsonResponse({
            "message": "object does not exist, most likely bad request"
        }, status=400)
    except KeyError:
        return JsonResponse({
            "message": "Item does not exist, most likely bad request"
            }, status=400)

    if quantity != int(quantity) or quantity <= 0:
        return JsonResponse({"message": "Illegal quantity value"}, status=400)

    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({"message": "cart_item quantity updated"}, status=200)
