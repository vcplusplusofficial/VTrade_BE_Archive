from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from . import user

# user views
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_operations(request, user_id=None):
    if request.method == 'GET':
        if user_id:
            response = user.get_user(user_id)
            return JsonResponse(response)
        else:
            return JsonResponse({"error": "User ID parameter is missing"}, status=400)

    elif request.method == 'POST':
        user_data = request.data
        if not user_data:
            return JsonResponse({"error": "No data provided"}, status=400)
        response = user.add_user(user_data)
        return JsonResponse(response)

    elif request.method == 'PUT':
        if not user_id:
            return JsonResponse({"error": "User ID parameter is missing"}, status=400)
        user_data = request.data
        if not user_data:
            return JsonResponse({"error": "No data provided"}, status=400)
        response = user.update_user(user_id, user_data)
        return JsonResponse(response)

    elif request.method == 'DELETE':
        if not user_id:
            return JsonResponse({"error": "User ID parameter is missing"}, status=400)
        response = user.delete_user(user_id)
        return JsonResponse(response)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@api_view(['GET', 'POST'])
def get_user(request):
    if request.method == 'GET':
        user_id = request.GET.get("user_id", "")
        return user_operations(request, user_id)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@api_view(['POST'])
def add_user(request):
    return user_operations(request)


@api_view(['PUT'])
def update_user(request, user_id):
    return user_operations(request, user_id)


@api_view(['DELETE'])
def remove_user(request, user_id):
    return user_operations(request, user_id)


@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        email = request.data.get("email", "")
        if not email:
            return JsonResponse({"error": "Email parameter is missing"}, status=400)
        response = user.forgot_password(email)
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        reset_token = request.data.get("reset_token", "")
        if not reset_token:
            return JsonResponse({"error": "Reset token parameter is missing"}, status=400)
        new_password = request.data.get("new_password", "")
        if not new_password:
            return JsonResponse({"error": "New password parameter is missing"}, status=400)
        response = user.reset_password(reset_token, new_password)
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
