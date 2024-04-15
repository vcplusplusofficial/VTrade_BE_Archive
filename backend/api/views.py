from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import listing

# View for listing operations
@api_view(['GET', 'POST'])
def listing_operations(request):
    if request.method == 'GET':
        user_input = request.GET.get("user_input", "").split("+")
        if not user_input:
            return Response({"error": "Input parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)

        operations = {
            'filter_price': listing.filter_price,
            'get_items': listing.get_items,
            'display_top_sale': listing.display_top_sale,
            'display_top_request': listing.display_top_request,
            'display_recent_post': listing.display_recent_post,
            'get_product_info': listing.get_product_info,
        }

        operation = user_input.pop(0)
        if operation not in operations:
            return Response({"error": "Invalid operation"}, status=status.HTTP_400_BAD_REQUEST)

        response = operations[operation](user_input)
        # Ensure response is serialized properly
        return Response(response)

    elif request.method == 'POST':
        # For POST, use request.data
        response = listing.post_listing(request.data)
        # Ensure response is serialized properly
        return Response(response, status=status.HTTP_201_CREATED)

    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# View for modifying a listing
@api_view(['DELETE', 'PUT'])
def modify_listing(request, listing_id):
    if request.method == 'DELETE':
        # Handle DELETE request to remove a listing
        pass  # Implement logic here if needed

    elif request.method == 'PUT':
        input_data = request.data
        if not input_data:
            return Response({"error": "Input data is missing"}, status=status.HTTP_400_BAD_REQUEST)

        is_buy_request = input_data.pop(0)  # Assuming the first item determines if it's a buy request
        if is_buy_request:
            response = listing.buy_product(input_data)
        else:
            response = listing.update_listing(input_data)

        return Response(response)

    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
