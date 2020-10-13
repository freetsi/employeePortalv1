import base64

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from rootapp.models import Report

# TEST FOR REPORT API
class ReportAPIViewTestCase(APITestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('test', 'lennon@thebeatles.com', 'testidios')

	def test_create_account(self):
		"""
		Ensure we can create a new report object.
		"""
		self.client.login(username='test', password='testidios')
		url = reverse('report')
		data = {
			"title": "PRO",
			"description": "Promoted on 13/10/2020",
			"user_id": self.user.id,
			"priority": "high",
			"solved": False
		}
		response = self.client.post(url, data, format='json')
		print(response.data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Report.objects.count(), 1)
		self.assertEqual(Report.objects.get().title, 'PRO')

