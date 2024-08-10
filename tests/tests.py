from django.test import TestCase
from sublets.models import User, Listing
from django.shortcuts import reverse


class TestSimplePagesWithLogin(TestCase):
    """
    Just test if a few pages properly load with good status codes.
    """
    def setUp(self):
        # TestCase has user as an attribute
        self.user = User.objects.create_user(
            username='test', password='t3$+123')
        # TestCase also has client as an attribute, so although we
        # made a Client() in class, this is not necessary and apparently
        # not as recommended as using TestCase.client.
        self.client.login(username='test', password='t3$+123')

        self.listing = Listing.objects.create(
            created_by=self.user,
            description="Test description",
            address_line_1="Test address",
            city="Boston Area",
            state="MA",
            zip_code="02108",
            rent=1000,
            listing_type="room_in_apartment",
            start_date="2024-09-01",
            end_date="2025-05-31",
            bedroom_count=1,
            bathroom_count="1"
        )

    def test_simple_page_loads(self):
        # Only includes pages that don't require kwargs
        # (e.g. ?city=Philadelphia)
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
                             f"status code {response.status_code}:" +
                             f"\n{page_name}")
            self.assertTrue(200 <= response.status_code < 400, error_message)
