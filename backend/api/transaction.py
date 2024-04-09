from rest_framework import status
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from .serializers import TransactionSerializer
from .models import Transaction
from django.http import JsonResponse


def add_transaction(transaction_data):
    try:
        price, listing_id, buyer_id, seller_id = transaction_data

        new_transaction = Transaction.objects.create(
            price=price,
            listing_id=listing_id,
            buyer_id=buyer_id,
            seller_id=seller_id
        )

        serializer = TransactionSerializer(new_transaction)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        return JsonResponse({"error": "Integrity error, possibly duplicate data."}, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError:
        return JsonResponse({"error": "Database error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        # Log the exception for debugging
        print(e)
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_transaction(transaction_id, transaction_data):
    try:
        transaction = Transaction.objects.get(pk=transaction_id)
        for field, value in transaction_data.items():
            if hasattr(transaction, field):
                setattr(transaction, field, value)
        transaction.save()
        return JsonResponse({"message": "Transaction updated successfully"})
    except Transaction.DoesNotExist:
        return JsonResponse({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Log the exception for debugging
        print(e)
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def remove_transaction(transaction_id):
    try:
        transaction = Transaction.objects.get(pk=transaction_id)
        transaction.delete()
        return JsonResponse({"message": "Transaction removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Transaction.DoesNotExist:
        return JsonResponse({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Log the exception for debugging
        print(e)
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_transaction(transaction_id):
    try:
        transaction = Transaction.objects.get(pk=transaction_id)
        serializer = TransactionSerializer(transaction)
        return JsonResponse(serializer.data)
    except Transaction.DoesNotExist:
        return JsonResponse({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Log the exception for debugging
        print(e)
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
