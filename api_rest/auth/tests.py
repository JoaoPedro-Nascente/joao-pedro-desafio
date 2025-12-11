from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

#Authentication Unit Tests
class AuthAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('user_register')
        self.login_url = reverse('token_obtain_pair')
        self.username = 'testUser'
        self.password = 'testPassword'
        self.valid_data = {
            'username': self.username,
            'password': self.password
        }

    def test_user_registration_success(self):
        innitial_count = User.objects.count()
        response = self.client.post(self.register_url, self.valid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), innitial_count + 1)
        self.assertIn('username', response.data)

    def test_user_registration_duplicate(self):
        self.client.post(self.register_url, self.valid_data, format='json')
        response = self.client.post(self.register_url, self.valid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_token_obtain_success(self):
        self.client.post(self.register_url, self.valid_data, format='json')

        response = self.client.post(self.login_url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)