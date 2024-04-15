from django.shortcuts import render
from django.http import JsonResponse
from .models import Listing
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .serializers import CardViewListingSerializer, DetailedListingSerializer
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from rest_framework import status


# used to create a new listing
def post_listing(user_input):
    try:
        user_id, listing_type, title, location, description, form, price, status, payment_method, category, condition = user_input

        # Create a new Listing object
        new_listing = Listing.objects.create(
            user_id=user_id,
            listing_type=listing_type,
            title=title,
            location=location,
            description=description,
            form=form,
            price=price,
            status=status,
            payment_method=payment_method,
            category=category,
            condition=condition,
        )

        serializer = DetailedListingSerializer(new_listing, many=True)
        return JsonResponse({'listing': serializer.data})
    except ValidationError as e:
        # Handle validation errors, e.g., missing fields or incorrect data types
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        # Handle errors related to the integrity of the database,
        # like unique constraint violations
        return JsonResponse({"error": "Integrity error, possibly duplicate data."}, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError:
        # Handle general database errors
        return JsonResponse({"error": "Database error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        # Catch-all for any other exceptions, should be logged for debugging.
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# used in category page, when filtering with price
def filter_price(user_input):
    if not user_input:
        return Listing.objects.all()  # Return all items if no price specified

    try:
        price = float(user_input[0])
    except ValueError:
        return JsonResponse({"error": "Invalid price format"}, status=status.HTTP_400_BAD_REQUEST)

    # Filter items with price less than the specified price
    filter_item = Listing.objects.filter(price__lt=price)

    return filter_item


# used to get listing based on category
def get_items(user_input):
    category = user_input
    try:
        listing = Listing.objects.get(category=category)
    except Listing.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    return listing


# used in the homepage, gets the most active sales
def display_top_sale():
    try:
        top_sale = Listing.objects.filter(form="provide").order_by("-clicked")[:10]
        serializer = CardViewListingSerializer(top_sale, many=True)
        return JsonResponse({'listing': serializer.data})
    except ObjectDoesNotExist:
        return []


# used in the homepage, gets the most active requests
def display_top_request():
    try:
        top_request = Listing.objects.filter(form="request").order_by("-clicked")[:10]
        serializer = CardViewListingSerializer(top_request, many=True)
        return JsonResponse({'listing': serializer.data})
    except ObjectDoesNotExist:
        return []


# used in the homepage, gets the most recent posts
def display_recent_post():
    try:
        recent_post = Listing.objects.order_by("-create_date")[:5]
        serializer = CardViewListingSerializer(recent_post, many=True)
        return JsonResponse({'listing': serializer.data})
    except ObjectDoesNotExist:
        return []


def remove_listing(user_input):
    return


def update_listing(user_input):
    return


# used when you click to view more details about a product
def get_product_info(user_input):
    id = user_input[0]
    try:
        listing = Listing.objects.get(id=id)
    except Listing.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    track_clicks(listing)
    return listing


# used to track activity
@transaction.atomic
def track_clicks(listing):
    listing.clicked += 1
    listing.save(update_fields=['clicked'])


# used when you buy a product
def buy_product(user_input):
    id = user_input[0]
    try:
        listing = Listing.objects.get(id=id)
    except Listing.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    listing.status = False
    listing.save()

    return listing

