from models import Transaction
from django.http import JsonResponse

def add_transaction(transaction_data):
    price, listing_id, buyer_id, seller_id= transaction_data
    
    new_transaction = Transaction(
        price=price,
        listing_id=listing_id,
        buyer_id=buyer_id,
        seller_id=seller_id
    )
    
    instance = Transaction.create(new_user)
    
    return JsonResponse({"message": "Transaction created successfully"})

def update_transaction(transaction_data):
    transaction = get_transaction(transaction_data)
    
    for field, value in transaction_data.items():
        if hasattr(transaction, field):
            setattr(transaction, field, value)
            
    transaction.save()
    
    return JsonResponse({"message": "Transaction updated successfully"})

def remove_transaction(transaction_data):
    transaction = get_transaction(transaction_data)
    
    transaction.delete()
    
    return JsonResponse({"message": "Transaction removed successfully"})
    
def get_transaction(transaction_data):
    transaction_id = transaction_data.get("id")
    
    try: 
        transaction = Transaction.objects.get(pk=transaction_id)
        return transaction
    except Transaction.DoesNotExist:
        return JsonResponse({"error": "Transaction not found"}, status=404)
