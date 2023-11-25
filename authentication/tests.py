from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class AccountUserManagerTests(TestCase):
    
    def test_create_user(self):
        USER_EMAIL = "normal@user.com"
        PASSWORD = "foo"

        User = get_user_model()
        user = User.objects.create_user(email=USER_EMAIL, password=PASSWORD)
        
        self.assertEqual(user.email, USER_EMAIL)
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")
        self.assertEqual(user.last_name, "")


        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(PASSWORD))

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
