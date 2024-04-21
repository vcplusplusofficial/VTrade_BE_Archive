from .models import User
import hashlib
from .serializers import UserSerializer
from rest_framework import status
from django.http import JsonResponse
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError, ObjectDoesNotExist


def add_user(user_input):
    try:
        first_name, last_name, class_year, email, username, password = user_input
        hashed_password = hashlib.sha256(password.replace(" ", "").encode()).hexdigest()

        # Create a new user object with the provided data
        new_user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_password,
            class_year=class_year,
        )

        serializer = UserSerializer(new_user)
        return JsonResponse({'user': serializer.data})
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


def update_user(user_input):
    try:
        # Parse the user input
        parsed_input = parse_user_input(user_input)

        # Get the user object to update
        user_id = parsed_input.get("id")  # Assuming 'id' is provided in user_input
        user = User.objects.get(pk=user_id)

        # Update the user object with the provided fields
        for field, value in parsed_input.items():
            if hasattr(user, field):
                setattr(user, field, value)

        # Save the updated user object
        user.save()

        return JsonResponse({"message": "User updated successfully"})
    except KeyError as e:
        # Handle missing key error
        return JsonResponse({"error": f"Missing key: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        # Handle case when user doesn't exist
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Catch-all for any other exceptions, should be logged for debugging.
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def parse_user_input(user_input):
    parsed_data = {}

    # implement logic for parsing
    # for value in user_input:

    return parsed_data


def get_user(user_input):
    try:
        id = user_input[0]
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return JsonResponse({'user': serializer.data})
    except IndexError:
        return JsonResponse({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def remove_user(user_input):
    try:
        id = user_input[0]
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse({"message": "User deleted successfully"})
    except IndexError:
        return JsonResponse({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def forgot_password(user_input):
    try:
        email = user_input
        user = User.objects.get(email=email)
        # Logic for forgot password
        return JsonResponse({"message": "Forgot password request processed"})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def reset_password(user_input):
    try:
        email, password = user_input
        user = User.objects.get(email=email)
        user.password = password
        user.save()
        return JsonResponse({"message": "User password updated successfully"})
    except ValueError:
        return JsonResponse({"error": "Email and password not provided"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
