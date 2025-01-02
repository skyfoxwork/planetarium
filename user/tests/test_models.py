from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model


class UserManagerTests(TestCase):
    def test_create_user_with_email(self):
        email = 'user@example.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        self.assertRaises(ValueError, get_user_model().objects.create_user, '', 'testpassword')


    def test_create_superuser(self):
        email = 'superuser@example.com'
        password = 'testpassword'
        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email='superuser@example.com',
                password='testpassword',
                is_superuser=False
            )


class UserModelTests(TestCase):
    def test_user_str_method(self):
        email = 'user@example.com'
        user = get_user_model().objects.create_user(email=email, password='testpassword')

        self.assertEqual(str(user), email)

    def test_user_email_unique(self):
        email = 'user@example.com'
        user1 = get_user_model().objects.create_user(email=email, password='testpassword')

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(email=email, password='anotherpassword')

    def test_user_password_set(self):
        email = 'user@example.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertTrue(user.check_password(password))
        self.assertFalse(user.check_password('wrongpassword'))
