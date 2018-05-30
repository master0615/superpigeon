from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from superpigeon.apps.api.models import UserProfile, TokenExpired, Organization, Product, Order
from rest_framework.authtoken.models import Token

from datetime import datetime, timezone, timedelta
import time

class APITests(APITestCase):
    def test_signup(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/signup/'
        data = {
            'email':'tester@tester.com',
            'password':'tester',
            'first_name': 'first name',
            'last_name': 'last name'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(username='tester@tester.com').count(), 1)
        self.assertEqual(User.objects.get(username='tester@tester.com').email, 'tester@tester.com')

    def test_signup_organization(self, **req):
        url = '/api/signup/'
        data = {
            'email':req.get('email', 'tester@tester.com'),
            'password':req.get('password', 'tester'),
            'first_name': req.get('first_name', 'first name'),
            'last_name': req.get('last_name', 'last name'),
            'business_name': req.get('business_name', 'DatePalm LCC'),
            'business_address': req.get('business_address', 'St. tester'),
            'business_phone': req.get('business_phone', '7654321')
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(username='tester@tester.com').count(), 1)
        self.assertEqual(User.objects.get(username='tester@tester.com').email, 'tester@tester.com')
        self.assertEqual(UserProfile.objects.filter(user__id=response.data['id']).count(), 1)
        self.assertEqual(Organization.objects.filter(user=UserProfile.objects.get(user__id=response.data['id'])).count(), 1)
        self.assertEqual(Organization.objects.filter(user=UserProfile.objects.get(user__id=response.data['id']))[0].phone, data['business_phone'])
        return response.data['id']

    def test_login_and_get_token(self):
        """
        Ensure we can login and get token with default expiration.
        """
        self.test_signup()
        url = '/api/auth/'
        data = {
            'email': 'tester@tester.com',
            'password':'tester',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TokenExpired.objects.filter(token__key=response.data['token']).count(), 1)
        return response.data['token']

    def test_logout_after_get_token(self):
        token = self.test_login_and_get_token()
        url = '/api/logout/'
        data = {
            'token': token
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TokenExpired.objects.filter(token__key=token).count(), 0)


    def test_login_and_get_custom_expire_token(self):
        self.test_signup()
        url = '/api/auth/'
        data = {
            'email': 'tester@tester.com',
            'password':'tester',
            'exp_sec': 10 #test with 10sec expiration
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TokenExpired.objects.filter(token__key=response.data['token'], exp__gte=datetime.now(timezone.utc)).count(), 1)
        time.sleep(15)
        # checking token after 15sec
        self.assertEqual(TokenExpired.objects.filter(token__key=response.data['token'], exp__gte=datetime.now(timezone.utc)).count(), 0)

    def test_hit_protected_api_urls_without_token(self):
        for i in settings.PROTECTED_URL:
            response_get = self.client.get(i, format='json')
            self.assertEqual(response_get.status_code, status.HTTP_403_FORBIDDEN)
            response_post = self.client.post(i, format='json')
            self.assertEqual(response_post.status_code, status.HTTP_403_FORBIDDEN)


    def test_hit_protected_api_urls_with_token(self):
        token = self.test_login_and_get_token()
        self.assertEqual(TokenExpired.objects.filter(token__key=token).count(), 1)
        for i in settings.PROTECTED_URL:
            response_get = self.client.get(i+'?token=%s' % token, format='json')
            self.assertEqual(response_get.status_code, status.HTTP_200_OK)
            response_post = self.client.post(i, {'token':token}, format='json')
            self.assertIn(response_post.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def test_renew_token_after_expired(self):
        self.test_signup()

        url = '/api/auth/'
        data = {
            'email': 'tester@tester.com',
            'password':'tester',
            'exp_sec': 10  # test with 10sec expiration
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TokenExpired.objects.filter(token__key=response.data['token']).count(), 1)
        token_first = response.data['token']
        time.sleep(5)

        url = '/api/auth/'
        data = {
            'email': 'tester@tester.com',
            'password':'tester',
            'exp_sec': 10  # test with 10sec expiration
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TokenExpired.objects.filter(token__key=response.data['token']).count(), 1)
        token_second = response.data['token']
        self.assertEqual(token_first, token_second)

        time.sleep(6)
        url = '/api/auth/'
        data = {
            'email': 'tester@tester.com',
            'password':'tester',
            'exp_sec': 10  # test with 10sec expiration
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TokenExpired.objects.filter(token__key=response.data['token']).count(), 1)
        token_third = response.data['token']

        self.assertNotEqual(token_first, token_third)

    def test_profile_update(self):
        token = self.test_login_and_get_token()

        url = '/api/profile/'
        data = {
            'email': 'tester@tester.com',
            'password':'tester',
            'token': token,
            'phone': '7654321',
            'address': 'address edited'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.filter(user__username=data['email'])[0].phone, data['phone'])
        self.assertEqual(UserProfile.objects.filter(user__username=data['email'])[0].address, data['address'])

    def test_organization_update(self):
        self.test_signup_organization()
        url = '/api/auth/'
        data = {
            'email': 'tester@tester.com',
            'password':'tester',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TokenExpired.objects.filter(token__key=response.data['token']).count(), 1)

        profile_url = '/api/profile/'
        data = {
            'token': response.data['token'],
            'business_name': 'edited',
            'business_address': 'edited',
            'business_phone': 'edited'
        }
        response_profile = self.client.post(profile_url, data, format='json')
        self.assertEqual(response_profile.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.get(user=UserProfile.objects.get(user__id=response.data['id'])).address,
                         data['business_address'])
        self.assertEqual(Organization.objects.get(user=UserProfile.objects.get(user__id=response.data['id'])).business_name,
                         data['business_name'])
        self.assertEqual(Organization.objects.get(user=UserProfile.objects.get(user__id=response.data['id'])).phone,
                         data['business_phone'])
        return response.data['token']

    def test_invite_admin_organization(self):
        token = self.test_organization_update()
        id_1 = self.test_signup_organization(email='tester10@tester.com', password='testertester', business_name='business test10')
        id_2 = self.test_signup_organization(email='tester11@tester.com', password='testertester', business_name='business test11')
        url = '/api/profile/'

        data = {
            'token':token,
            'admins': [id_1, id_2],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.get(user=UserProfile.objects.get(user=Token.objects.get(key=token).user)).admins.all().count() , 2)

    def test_uninvite_admin_organization(self):
        token = self.test_organization_update()
        id_1 = self.test_signup_organization(email='tester10@tester.com', password='testertester', business_name='business test10')
        id_2 = self.test_signup_organization(email='tester11@tester.com', password='testertester', business_name='business test11')
        url = '/api/profile/'

        data = {
            'token':token,
            'admins': [id_1, id_2],
        }
        self.client.post(url, data, format='json')

        data = {
            'token':token,
            'remove_admins': [id_1, id_2],
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.get(user=UserProfile.objects.get(user=Token.objects.get(key=token).user)).admins.all().count() , 0)


    def test_product_sync(self):
        url = '/api/sync_product/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data.keys())
        self.assertNotEqual(Product.objects.all().count(), 0)

    def test_order_sync(self):
        url = '/api/sync_order/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data.keys())
        self.assertNotEqual(Order.objects.all().count(), 0)