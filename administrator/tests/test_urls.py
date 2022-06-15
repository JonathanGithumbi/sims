from audioop import reverse
from http import client
from django.test import TestCase, Client
from django.urls import reverse
#i add a test class for each view i want to test 

class TestAdministratorUrls(TestCase):
    """This class will test that all of the urls for the admin app are functional"""
    def setUp(self):
        self.client= Client()
        self.client.post(reverse('login'), {'username':'administrator1@localhost.com','password':'nAN01300m'})
        
    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)



