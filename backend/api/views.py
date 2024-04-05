from django.shortcuts import render
from django.http import JsonResponse
from . import user, transaction

# Create your views here.

# Transaction views
def get_transaction(request):
    transaction_data = request.GET.get("transaction_data", "").split("+")
    if not transaction_data:
        return JsonResponse({"error": "Input parameter is missing"}, status=400)
    
    response = transaction.get_transaction(transaction_data)
    
    return JsonResponse(response)


    