from apps.players.models import Player
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.players.tests.factories import DEFAULT_PASSWORD, PlayerFactory
from apps.players.serializers import PlayerReadSerializer

from .checkers import AuthTesting


class Test_Login_View(AuthTesting):

    def test_correct_login_no_data(self):
        """Testing a legitimate login."""
        userModel = PlayerFactory()
        data = {'email': userModel.email, 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('login')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'token': str(Token.objects.get(user=userModel)),
            'player': PlayerReadSerializer(userModel).data
        }
        self.assertEqual(correctResponse, responseData)

    def test_correct_login_one_other_user(self):
        """Testing a legitimate login with one other user."""
        userModel = PlayerFactory()
        PlayerFactory()
        data = {'email': userModel.email, 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('login')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'token': str(Token.objects.get(user=userModel)),
            'player': PlayerReadSerializer(userModel).data
        }
        self.assertEqual(correctResponse, responseData)

    def test_login_bad_email(self):
        """Testing a bad login with bad email param."""
        data = {'email': 'test', 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('login')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'email': ['Enter a valid email address.']}
        self.assertEqual(correctResponse, responseData)

    def test_login_no_email(self):
        """Testing a bad login with no email param."""
        data = {'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('login')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'email': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_login_no_password(self):
        """Testing a bad login with no password param."""
        data = {'email': 'willFail@gmail.com'}

        client = APIClient()
        url = reverse('login')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'password': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_login_no_email_or_password(self):
        """Testing a bad login with no email or password params."""
        data = {}

        client = APIClient()
        url = reverse('login')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'password': ['This field is required.'],
            'email': ['This field is required.']
        }
        self.assertEqual(correctResponse, responseData)
