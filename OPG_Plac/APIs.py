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


# Stores Users delivery data and creates or modifies Order obj with a null status
def store_delivery_data(request):  # This Order obj is used as a tmp info storage until user completes/confirms order
    if request.method != "POST" or not request.user.is_authenticated:
        return JsonResponse({"message": "bad_request"}, status=400)

    user = models.User.objects.get(email=request.user)

    try:    # Get or create Order obj
        order = user.orders.get(status=None)            # TODO Improve server-side validation - Boolean options are hazard currently if blank data received
    except ObjectDoesNotExist:
        order = models.Order(user=user)

    try:  # Load data into obj
        json_data = json.loads(request.body)

        user_info = json_data["user_info"]
        delivery_info = json_data["delivery_info"]
        company_info = json_data["company_info"]

        remember_input = json_data["remember"]

        same_delivery = json_data["same_delivery"]
        need_R1 = json_data["need_r1"]

        order.same_delivery = same_delivery
        order.need_R1 = need_R1

        order.first_name = user_info["first_name"]
        order.last_name = user_info["last_name"]

        order.address = user_info["address"]
        order.place = user_info["place"]
        order.post_code = user_info["post_code"]
        order.phone = user_info["phone"]

        order.delivery_first_name = delivery_info["delivery_name"]
        order.delivery_last_name = delivery_info["delivery_surname"]
        order.delivery_address = delivery_info["delivery_address"]
        order.delivery_post_code = delivery_info["delivery_post_code"]
        order.delivery_place = delivery_info["delivery_place"]
        order.delivery_phone = delivery_info["delivery_phone"]

        order.company_name = company_info["company_name"]
        order.company_address = company_info["company_address"]
        order.company_post_code = company_info["company_post_code"]
        order.OIB = company_info["OIB"]

        order.notice = json_data["notice"].strip()  # Store notice without leading and trailing whitespaces

    except KeyError:
        return JsonResponse({"message": "bad_request"}, status=400)

    order.save()

    # Store user data for future Orders
    if remember_input:
        try:
            extended_info = user.extendeduser
        except ObjectDoesNotExist:
            extended_info = models.ExtendedUser(user=user)

        user.first_name = user_info["first_name"]
        user.last_name = user_info["last_name"]

        extended_info.address = user_info["address"]
        extended_info.place = user_info["place"]
        extended_info.post_code = user_info["post_code"]
        extended_info.phone = user_info["phone"]

        extended_info.delivery_first_name = delivery_info["delivery_name"]
        extended_info.delivery_last_name = delivery_info["delivery_surname"]
        extended_info.delivery_address = delivery_info["delivery_address"]
        extended_info.delivery_post_code = delivery_info["delivery_post_code"]
        extended_info.delivery_place = delivery_info["delivery_place"]
        extended_info.delivery_phone = delivery_info["delivery_phone"]

        extended_info.company_name = company_info["company_name"]
        extended_info.company_address = company_info["company_address"]
        extended_info.company_post_code = company_info["company_post_code"]
        extended_info.OIB = company_info["OIB"]

        extended_info.same_delivery = same_delivery
        extended_info.need_R1 = need_R1

        extended_info.save()

    return JsonResponse({}, status=200)


def create_order(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return JsonResponse({"message": "bad_request"}, status=400)

    # Get user and cart -- assume authorised due to check above
    user = models.User.objects.get(email=request.user)
    cart = user.cart.all()

    if len(cart) == 0:  # If no items in cart, probably bad or malicious request
        return JsonResponse({"message": "Probably bad request"}, status=400)

    try:  # Get Order obj with status None -- Created when user submits delivery data
        order = user.orders.get(status=None)

        payment_reference = json.loads(request.body)["payment_option"]
        payment = models.PaymentOption.objects.get(reference=payment_reference)
    except ObjectDoesNotExist:  # Not possible to reach checkout without submitting delivery data, hence creating None status Order obj
        return JsonResponse({"message": "Probably bad request"}, status=400)
    except KeyError:  # payment_reference must be included in json payload
        return JsonResponse({"message": "Probably bad request"}, status=400)

    for item in cart:  # Create order_item objs for every item in cart
        order_item = models.OrderItem(
            order=order,
            product=item.product,
            quantity=item.quantity
        )
        order_item.archive_product()  # Archive product data
        order_item.save()      # Store order_item obj

        item.delete()  # Clear processed items from cart

    # Mark order as confirmed -- set initial processing status
    status = models.OrderStatus.objects.get(status="Zaprimljeno")
    order.status = status
    order.paymentOption = payment  # Set chosen payment model

    # Save history
    order_history = models.OrderHistory(order=order, status=status)
    order_history.save()

    order.save()  # Save order

    return JsonResponse({"message": "order confirmed and processed"}, status=200)
