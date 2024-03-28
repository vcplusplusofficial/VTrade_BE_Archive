from django.shortcuts import render
from django.http import JsonResponse
from . import user

# Create your views here.

#user views
def get_user(request):
    user_input = request.GET.get("user_input", "").split("+")
    if not user_input:
        return JsonResponse({"error": "Input parameter is missing"}, status=400)

    response = user.get_user(user_input)
    return JsonResponse(response)


def add_user(request):
    user_input = request.GET.get("user_input", "")
    if not user_input:
        return JsonResponse({"error": "Input parameter is missing"}, status=400)

    response = user.add_user(user_input)

    return JsonResponse(response)


def update_user(request):
    user_input = request.GET.get("user_input", "")
    if not user_input:
        return JsonResponse({"error": "Input parameter is missing"}, status=400)

    response = user.update_user(user_input)

    return JsonResponse(response)


def remove_user(request):
    user_input = request.GET.get("user_input", "")
    if not user_input:
        return JsonResponse({"error": "Input parameter is missing"}, status=400)

    response = user.delete_user(user_input)

    return JsonResponse(response)


def forgot_password(request):
    user_input = request.GET.get("user_input", "")
    if not user_input:
        return JsonResponse({"error": "Input parameter is missing"}, status=400)

    response = user.forgot_password(user_input)

    return JsonResponse(response)


def reset_password(request):
    user_input = request.GET.get("user_input", "")
    if not user_input:
        return JsonResponse({"error": "Input parameter is missing"}, status=400)

    response = user.reset_password(user_input)

    return JsonResponse(response)

