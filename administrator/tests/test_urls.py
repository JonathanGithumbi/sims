from audioop import reverse
from http import client
from django.test import TestCase
from django.urls import reverse
#i add a test class for each view i want to test 

class TestAdministratorUrls(TestCase):
    """This class will test that all of the urls for the admin app are functional"""
    def setUp(self):
        # setup models 
        pass

    def test_admin_dashboard(self):
        response = self.client.get(reverse('administrator_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_register_student(self):
        response = self.client.get(reverse('register_student'))
        self.assertEqual(response.status_code, 200)
