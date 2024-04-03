from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import listing


@api_view(['GET', 'POST'])
def listing_operations(request):
    if request.method == 'GET':
        user_input = request.GET.get("user_input", "").split("+")
        if not user_input:
            return Response({"error": "Input parameter is missing"}, status=400)

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
            return Response({"error": "Invalid operation"}, status=400)

        response = operations[operation](user_input)
        # Ensure response is serialized properly
        return Response(response)

    elif request.method == 'POST':
        # For POST, use request.data
        response = listing.post_listing(request.data)
        # Ensure response is serialized properly
        return Response(response)

    else:
        return Response({"error": "Method not allowed"}, status=405)


@api_view(['DELETE', 'PUT'])
def modify_listing(request, listing_id):
    if request.method == 'DELETE':
        # Handle DELETE request to remove a listing
        pass

    elif request.method == 'PUT':
        user_input = request.GET.get("user_input", "").split("+")
        if not user_input:
            return Response({"error": "Input parameter is missing"}, status=400)

        if user_input[0].pop(0):
            response = listing.buy_product(user_input)
        else:
            response = listing.update_listing(user_input)

        return Response(response)
