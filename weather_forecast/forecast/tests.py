from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import SearchHistory, Profile
from .forms import UserRegisterForm

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, bio='Test Bio')

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'Test Bio')

class SearchHistoryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.search_history = SearchHistory.objects.create(
            user=self.user,
            city='Test City',
            temperature=25,
            description='Sunny',
            humidity=50
        )

    def test_search_history_creation(self):
        self.assertEqual(self.search_history.user.username, 'testuser')
        self.assertEqual(self.search_history.city, 'Test City')
        self.assertEqual(self.search_history.temperature, 25)
        self.assertEqual(self.search_history.description, 'Sunny')
        self.assertEqual(self.search_history.humidity, 50)

class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_home_view_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/', {'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('weather', response.context)

class RegisterViewTestCase(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_form_invalid(self):
        form = UserRegisterForm(data={
            'username': '',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        })
        self.assertFalse(form.is_valid())

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_profile_view_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')




