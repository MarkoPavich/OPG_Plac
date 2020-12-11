from django.http import JsonResponse
from OPG_Plac import models
import json
import time


def create_user(request):

	if request.method != "POST":
		return JsonResponse({
			"message": f"Expected POST request, got '{request.method}'"
			}, status=400)

	json_data = json.loads(request.body)

	user = models.User(
		first_name=json_data["first_name"],
		last_name=json_data["last_name"],
		email=json_data["email"],
		password=json_data["password"] 
		)

	return JsonResponse({
		"message": "User created",
		}, status=200)
















