from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import os
import pathlib
from sublets.models import User, Listing, Message

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()


class MySeleniumTest(StaticLiveServerTestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', password='t3$+123')
        self.user2 = User.objects.create_user(username='test2', password='t3$+123')
        self.client.login(username='test1', password='t3$+123')

        self.listing = Listing.objects.create(
            created_by=self.user1,
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

        self.message = Message.objects.create(
            sender=self.user2,
            recipient=self.user1,
            listing=self.listing,
            body="Test message body"
        )
        
        # Get selenium ready and logged in
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 8)
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url)
        self.driver.add_cookie(
            {
                'name': 'sessionid', 
                'value': cookie.value, 
                'secure': False,
                'path': '/'
            })
        

    def tearDown(self):
        self.driver.quit()


    def test_message_reply(self):
        uri = self.live_server_url + '/message/'
        self.driver.get(uri)
        
        reply_button = self.wait.until(
            lambda x: x.find_element(By.CLASS_NAME, "message_button"))
        time.sleep(1) # For fun, to see what happens, I leave these in.
        reply_button.click()
        
        respond_div = self.wait.until(
            lambda x: x.find_element(By.ID, "respond")
        )
        time.sleep(1) # For fun, to see what happens, I leave these in.
        display = respond_div.value_of_css_property("display")
        self.assertEqual(display, "block")
        