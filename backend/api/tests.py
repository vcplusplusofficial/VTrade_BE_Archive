from django.test import TestCase, Client
from django.urls import reverse

class ListingViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_listing_operations_GET(self):
        # Test GET request to listing_operations view
        response = self.client.get(reverse('listing_operations'), {'user_input': 'filter_price+10'})
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on expected behavior

    def test_listing_operations_POST(self):
        # Test POST request to listing_operations view
        data = {
            'user_id': 1,
            'listing_type': True,
            'title': 'Test Listing',
            'location': 'Test Location',
            'description': 'Test Description',
            'form': False,
            'price': 10.0,
            'status': 1,
            'payment_method': 'Cash',
            'category': 'Test Category',
            'condition': 'New'
        }
        response = self.client.post(reverse('listing_operations'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on expected behavior

    def test_modify_listing_PUT(self):
        # Test PUT request to modify_listing view
        listing_id = 1
        data = {
            'user_input': ['buy_product', str(listing_id)]
        }
        response = self.client.put(reverse('modify_listing', kwargs={'listing_id': listing_id}), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on expected behavior

    def test_listing_operations_invalid_operation(self):
        # Test for an invalid operation in listing_operations view
        response = self.client.get(reverse('listing_operations'), {'user_input': 'invalid_operation'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid operation", response.content)

    def test_listing_operations_invalid_method(self):
        # Test for an invalid HTTP method in listing_operations view
        response = self.client.put(reverse('listing_operations'))
        self.assertEqual(response.status_code, 405)
        self.assertIn(b"Method not allowed", response.content)

    def test_post_listing_missing_fields(self):
        # Test for POST request to post_listing view with missing fields
        data = {
            'user_id': 1,
            'title': 'Test Listing',
            # Missing other required fields
        }
        response = self.client.post(reverse('listing_operations'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing fields", response.content)

    # def test_modify_listing_DELETE(self):
    #     # Test DELETE request to modify_listing view
    #     listing_id = 1
    #     response = self.client.delete(reverse('modify_listing', kwargs={'listing_id': listing_id}))
    #     self.assertEqual(response.status_code, 405)  # Method not allowed
    #     # Add more assertions based on expected behavior

    def test_get_product_info_not_found(self):
        # Test for a product not found in get_product_info view
        response = self.client.get(reverse('listing_operations') + f'?user_input=get_product_info+123')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"User not found", response.content)

