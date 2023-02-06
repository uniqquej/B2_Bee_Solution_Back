from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User

class UserRegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse('user_create_view')
        user_data = {
            "username" : "test1",
            "password" : "xptmxm123!",
            "password2" : "xptmxm123!"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)
    

class LoginTest(APITestCase):
    def setUp(self):
        self.data = { "username" : "test1","password" : "xptmxm123!"}
        self.user = User.objects.create_user('test1','xptmxm123!')
    
    def test_login(self):
        url = reverse('user_auth_view')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 200)
    
    def test_get_user(self):
        url = reverse('user_auth_view')
        access_token = self.client.post(url, self.data).data['access']
        response = self.client.get(
            path = url,
            HTTP_AUTHORIZATION = f'Bearer {access_token}'
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data['username'], self.data['username'])