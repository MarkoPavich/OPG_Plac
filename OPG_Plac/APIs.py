from django.http import JsonResponse
from django.db import IntegrityError
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

	except KeyError: 	# Catch no input data
		return JsonResponse({
			"message": "Bad input data"
		}, status=400)

	except IntegrityError:		# Catch email already exists
		return JsonResponse({
			"message": "Email already exists",
			"error": "mail_already_exists"
		}, status=400)

	user = authenticate(request, email=user.email, password=json_data["password"])
	login(request, user)

	return JsonResponse({		# If all checks out, send OK
		"message": "User created, and logged in"
		}, status=200)
