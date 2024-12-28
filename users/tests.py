import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup() 

import pytest
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserViewSetTestCase(APITestCase):
    @pytest.mark.django_db
    def test_create_user(self):
        client = APIClient()
        user_data = {
            "username": "testuser",
            "password": "password123",
            "name": "Test",
            "surname": "User",
        }

        response = client.post('/api/users/', user_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        assert response.data['username'] == user_data['username']
        assert response.data['name'] == user_data['name']
        assert response.data['surname'] == user_data['surname']
        assert 'password' not in response.data