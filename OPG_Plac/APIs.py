from django.http import JsonResponse
from OPG_Plac import models
import json
import time


def create_user(request):
    json_data = json.loads(request.body)

    print(json_data)

    return JsonResponse({
        "message": "Mail already exists",
    }, status=400)
















