from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import transaction


@api_view(['POST'])
def add_transaction_view(request):
    try:
        # Extract transaction data from request
        price = request.POST.get('price')
        listing_id = request.POST.get('listing_id')
        buyer_id = request.POST.get('buyer_id')
        seller_id = request.POST.get('seller_id')

        # Check if required fields are present
        if None in [price, listing_id, buyer_id, seller_id]:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare transaction data dictionary
        transaction_data = {
            'price': price,
            'listing_id': listing_id,
            'buyer_id': buyer_id,
            'seller_id': seller_id
        }

        # Call the add_transaction function from the transaction module
        response = transaction.add_transaction(transaction_data)
        return Response(response)
    except Exception as e:
        # Log the exception for debugging
        print(e)
        return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def transaction_detail(request):
    try:
        # Extract transaction ID from request parameters
        transaction_id = request.GET.get("user_input")
        if not transaction_id:
            return Response({"error": "Transaction ID is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse other fields if present
        transaction_data = request.GET.get("user_input", "").split("+")[1:]

        # Check HTTP method and call the appropriate function from the transaction module
        if request.method == 'GET':
            response = transaction.get_transaction(transaction_id)
        elif request.method == 'PUT':
            response = transaction.update_transaction(transaction_id, transaction_data)
        elif request.method == 'DELETE':
            response = transaction.remove_transaction(transaction_id)

        return Response(response)
    except Exception as e:
        # Log the exception for debugging
        print(e)
        return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
