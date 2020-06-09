from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


bill_data = {'username': "Bill",
            'email': "bill@google.com",
            'password':"123"}

leo_data = {'username': "Leo",
            'email': "leo@google.com",
            'password':"123"}

# Create your tests here.
class UserTests(APITestCase):

    def setUp(self):
        # Register user
        url = '/api/register/'
        data = {'username': "Bill",
                'email': "bill@google.com",
                'password':"123"}
        response = self.client.post(url, data)
    
    def test_registration(self):
        url = '/api/register/'
        data = leo_data
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(pk=2).username, data['username'])
        self.assertEqual(Token.objects.count(), 2)

    def test_login(self):
        url = '/api/login/'
        data = {'username': bill_data['username'],
                'password': bill_data['password']}
        response = self.client.post(url, data)
        retrieved_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieved_data['token'], str(Token.objects.get(user__username=bill_data['username'])))
    
    