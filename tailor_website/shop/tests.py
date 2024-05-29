from django.test import TestCase
from django.contrib.auth.models import User
from .models import Dress, Measurement, Tailor
from django.urls import reverse

class ShopTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.tailor = Tailor.objects.create(user=self.user, bio='Test bio')
        self.dress = Dress.objects.create(name='Test Dress', description='Test description', price=100.00, tailor=self.tailor)

    def test_dress_creation(self):
        dress = Dress.objects.get(name='Test Dress')
        self.assertEqual(dress.name, 'Test Dress', msg="Dress name doesn't match")
        self.assertEqual(dress.price, 100.00, msg="Dress price doesn't match")
        self.assertEqual(dress.tailor, self.tailor, msg="Dress tailor doesn't match")

    def test_measurement_submission(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(f'/submit_measurements/{self.dress.id}/', {'measurements': '{"waist": "32", "chest": "40"}'})
        self.assertEqual(response.status_code, 302, msg="Measurement submission failed")
        measurement = Measurement.objects.get(user=self.user, dress=self.dress)
        self.assertEqual(measurement.measurements, '{"waist": "32", "chest": "40"}', msg="Measurement data doesn't match")

class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')

    def test_signup(self):
        response = self.client.post(reverse('register'), {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'test123test123', 'password2': 'test123test123'})
        self.assertEqual(response.status_code, 302, msg="Signup failed")
        self.assertTrue(User.objects.filter(username='newuser').exists(), msg="User creation failed")

    def test_signup_invalid_data(self):
        response = self.client.post(reverse('register'), {'username': 'newuser', 'email': 'invalidemail', 'password1': 'test123', 'password2': 'test123'})
        self.assertEqual(response.status_code, 200, msg="Invalid data signup, didn't return OK")
        self.assertFalse(User.objects.filter(username='newuser').exists(), msg="Invalid data signup created a user")

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302, msg="Login failed")
        self.assertTrue('_auth_user_id' in self.client.session, msg="User not logged in")

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200, msg="Login with invalid credentials, didn't return OK")
        self.assertFalse('_auth_user_id' in self.client.session, msg="User logged in with invalid credentials")

    def test_logout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302, msg="Logout failed")
        self.assertFalse('_auth_user_id' in self.client.session, msg="User not logged out")
