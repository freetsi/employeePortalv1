from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase

from rootapp.models import Report, Department


# TEST FOR REPORT, EMPLOYEE API
class EmployeeAPIViewTestCase(APITestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('test', 'lennon@thebeatles.com', 'test')
		self.client.login(username='test', password='test')

	def test_create_account(self):
		"""
		Ensure we can create a new employee and report object.
		"""
		# self.client.login(username='test', password='test')
		employee_api_url = reverse('employee')
		report_api_url = reverse('report')
		self.department = Department.objects.create(name='Administration')
		employee_data = {
			"username": "ehantaki",
			"email": "ehantaki@der.com",
			"gender": "female",
			"title": "manager",
			"firstName": "Eleni",
			"lastName": "Handaki",
			"fatherName": "Panagiotis",
			"department": self.department.name,
			"birthDate": "23/12/1965",
			"phone": "210459988",
			"mobile": "698556644",
			"address": "Ag.Dimitriou 66",
			"postcode": "13234",
			"password": "manager123"
		}
		employee_response = self.client.post(employee_api_url, employee_data, format='json')
		print("Employee Api Response: " + str(employee_response.data))
		my_user = User.objects.get(username = 'ehantaki')

		report_data1 = {
			"title": "PRO",
			"description": "Promoted on 13/10/2020",
			"user_id": my_user.id,
			"priority": "high",
			"solved": False
		}

		report_data2 = {
			"title": "CON",
			"description": "New laptop",
			"user_id": my_user.id,
			"priority": "low",
			"solved": False
		}

		report_response1 = self.client.post(report_api_url, report_data1, format='json')
		report_response2 = self.client.post(report_api_url, report_data2, format='json')

		print("Report Api1 Response: " + str(report_response1.data))
		print("Report Api2 Response: " + str(report_response2.data))

		# Test that employee was insterted in the DB
		self.assertEqual(employee_response.status_code, 200)
		# Test that report 1 was inserted in DB after user ehantaki
		self.assertEqual(report_response1.status_code, 200)
		# Test that report 1 was inserted in DB after user ehantaki
		self.assertEqual(report_response2.status_code, 200)
		# Test that there are only 2 report entries
		self.assertEqual(Report.objects.count(), 2)
		# Test that there are only 2 users
		self.assertEqual(User.objects.count(), 2)

		fetch_reports_url = reverse('report_fetch') + '?username=ehantaki'
		fetch_report = self.client.get(fetch_reports_url)
		# Test that fetch reports api works properly
		self.assertEqual(len(fetch_report.data['body']), 2)


