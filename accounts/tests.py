from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class AccountTests(APITestCase):

    def setUp(self):
        """
        Runs before every test.

        Creates one user that can be reused by tests involving
        authentication.
        """

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )

    # ---------------------------------------------------------
    # REGISTRATION
    # ---------------------------------------------------------

    def test_user_registration(self):
        """
        A new user should be successfully registered.
        """

        url = reverse("register")

        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPassword123"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the user actually exists in the database
        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )

    def test_registration_duplicate_username(self):
        """
        Username must be unique.
        """

        url = reverse("register")

        data = {
            "username": "testuser",
            "email": "another@example.com",
            "password": "NewPassword123"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_duplicate_email(self):
        """
        Email must be unique.
        """

        url = reverse("register")

        data = {
            "username": "anotheruser",
            "email": "test@example.com",
            "password": "NewPassword123"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------------------------------------------------------
    # LOGIN / JWT
    # ---------------------------------------------------------

    def test_login_returns_tokens(self):
        """
        Valid credentials should return access and refresh tokens.
        """

        url = reverse("login")

        data = {
            "username": "testuser",
            "password": "TestPassword123"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_wrong_password(self):
        """
        Invalid password should not return JWT tokens.
        """

        url = reverse("login")

        data = {
            "username": "testuser",
            "password": "WrongPassword"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertNotIn("access", response.data)

    def test_login_with_nonexistent_user(self):
        """
        A user that doesn't exist should not be authenticated.
        """

        url = reverse("login")

        data = {
            "username": "doesnotexist",
            "password": "TestPassword123"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    # ---------------------------------------------------------
    # ME ENDPOINT
    # ---------------------------------------------------------

    def test_me_requires_authentication(self):
        """
        /me/ should reject unauthenticated requests.
        """

        url = reverse("me")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_user_can_access_me(self):
        """
        An authenticated user should be able to retrieve their profile.
        """

        refresh = RefreshToken.for_user(self.user)

        access_token = str(refresh.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        url = reverse("me")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["username"],
            "testuser"
        )

        self.assertEqual(
            response.data["email"],
            "test@example.com"
        )

    # ---------------------------------------------------------
    # TOKEN REFRESH
    # ---------------------------------------------------------

    def test_refresh_token_returns_new_access_token(self):
        """
        A valid refresh token should generate a new access token.
        """

        refresh = RefreshToken.for_user(self.user)

        url = reverse("refresh")

        data = {
            "refresh": str(refresh)
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("access", response.data)

    def test_refresh_with_invalid_token(self):
        """
        An invalid refresh token should be rejected.
        """

        url = reverse("refresh")

        data = {
            "refresh": "invalid-refresh-token"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    # ---------------------------------------------------------
    # LOGOUT / BLACKLIST
    # ---------------------------------------------------------

    def test_logout_blacklists_refresh_token(self):
        """
        The refresh token should be blacklisted after logout.
        """

        refresh = RefreshToken.for_user(self.user)

        refresh_token = str(refresh)

        url = reverse("logout")

        data = {
            "refresh": refresh_token
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        refresh_response = self.client.post(
            reverse("refresh"),
            {"refresh": refresh_token}
        )

        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_home(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Welcome to TeamTask API")

    def test_user_str(self):
        user = User.objects.create_user(
            username="strtest",
            email="strtest@example.com",
            password="TestPassword123"
        )

        self.assertEqual(str(user), "strtest")
