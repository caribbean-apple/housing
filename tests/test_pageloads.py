from django.test import TestCase
from sublets.models import User, UserProfile, Listing
from django.shortcuts import reverse

class TestSimplePagesWithLogin(TestCase):
    def setUp(self):
        # TestCase has user as an attribute
        self.user = User.objects.create_user(username='test_user', password='t3$+123')
        # TestCase also has client as an attribute, so although we
        # made a Client() in class, this is not necessary and apparently
        # not as recommended as using TestCase.client.
        self.client.login(username='test_user', password='t3$+123')

    def test_simple_page_loads(self):
        # Only includes pages that don't require kwargs (e.g. ?city=Philadelphia)
        # or URL parameters (e.g. /listing/<int:listing_id>/)
        simple_page_names = [
            "index",
            "create",
            "messages",
            "profile_setup",
            "robots",
            "logout"
        ]
        
        for page_name in simple_page_names:
            response = self.client.get(reverse(page_name))
            error_message = ("The following page returned " +
                f"status code {response.status_code}:\n{page_name}")
            self.assertTrue(200 <= response.status_code < 400, error_message)
