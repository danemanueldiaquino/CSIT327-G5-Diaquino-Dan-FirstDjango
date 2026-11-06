from django.test import TestCase
from django.urls import reverse

from .models import CustomerUser


class AccountViewsTests(TestCase):
    def test_signup_shows_success_message_after_creation(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newstudent",
                "email": "student@example.com",
                "first_name": "New",
                "last_name": "Student",
                "course": "Science",
                "password1": "StrongPass123!x",
                "password2": "StrongPass123!x",
            },
            follow=True,
        )

        self.assertTrue(CustomerUser.objects.filter(username="newstudent").exists())
        self.assertContains(response, "Your account has been created successfully.")

    def test_profile_update_is_limited_to_signed_in_user(self):
        user = CustomerUser.objects.create_user(
            username="student",
            password="StrongPass123!x",
            course="Science",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("profile"),
            {
                "username": "student",
                "email": "updated@example.com",
                "first_name": "Updated",
                "last_name": "Student",
                "course": "Arts",
            },
            follow=True,
        )

        user.refresh_from_db()
        self.assertEqual(user.email, "updated@example.com")
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.course, "Arts")
        self.assertContains(response, "Your profile was updated successfully.")

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
        )
