from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
User = get_user_model()


class UsersManagersTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="test@test.com", password="test@123")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create(email="", password="foo")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="test@admin.com", password="admin@123"
        )
        self.assertEqual(admin_user.email, "test@admin.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="test@admin.com", password="foo", is_superuser=False
            )
