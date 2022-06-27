import csv
import json
import logging
import re
import traceback
import pandas as pd

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from employees import settings
from rootapp.forms import EmployeeForm, ReportForm, FetchReportForm
from rootapp.functions import process_general_form_errors
from rootapp.models import Report
from rootapp.serializers import EmployeeApiSerializer, ErrorSerializer, SucessResponseSerializer, ReportApiSerializer, \
	SystemErrorSerializer, FetchReportsResponseSerializer, FetchReportsSerializer

logger = logging.getLogger(__name__)


#
# API 1 Storage of at least one report per employee in a local database.
#
class EmployeesApiView(GenericAPIView):
	""" Create/Update employees """

	permission_classes = (IsAuthenticated,)
	serializer_class = EmployeeApiSerializer

	@swagger_auto_schema(
		operation_summary="Initiate/Update Employee Record ",
		responses={
			'200': SucessResponseSerializer,
			'422': ErrorSerializer,
			'500': SystemErrorSerializer})
	def post(self, request, *args, **kwargs):
		request_dict = request.data.copy()
		form = EmployeeForm(request_dict)
		if form.is_valid():
			try:
				my_user, created = User.objects.update_or_create(username=request_dict["username"],
																 defaults={"email": request_dict["username"],
																		   "password": request_dict["password"],
																		   "first_name": request_dict["firstName"],
																		   "last_name": request_dict["lastName"]})
				my_user.profile.gender = request_dict["gender"]
				my_user.profile.title = request_dict["title"]
				my_user.profile.department = form.my_dep
				my_user.profile.birthDate = request_dict.get("birthDate", None)
				my_user.profile.phone = request_dict.get("phone", None)
				my_user.profile.mobile = request_dict.get("mobile", None)
				my_user.profile.address = request_dict.get("address", None)
				my_user.profile.father_name = request_dict.get("fatherName", None)
				my_user.profile.postcode = request_dict.get("postcode", None)
				my_user.save()
				if created:
					message = 'created'
				else:
					message = 'updated'
				my_reports = Report.objects.filter(user=my_user)
				notify = ''
				if not my_reports:
					notify = " This user has no reports. Please add them through <<reports>> API"
				return Response({"detail": "Employee with username {} and id {} was {}.".
								format(request_dict["username"], my_user.id, message) + notify}, status=200,
								content_type="application/json")
			except Exception:
				logger.critical(traceback.format_exc())
				return Response({"detail": "Error in api: {}".format(traceback.format_exc())}, status=500, content_type="application/json")
		else:
			logger.error(process_general_form_errors(json.loads(form.errors.as_json())))
			return Response(process_general_form_errors(json.loads(form.errors.as_json())),
							content_type="application/json", status=422)


#
# API 2 Storage of at least one report per employee in a local database.
#
class ReportsApiView(GenericAPIView):
	""" Create/Update reports """

	permission_classes = (IsAuthenticated,)
	serializer_class = ReportApiSerializer

	@swagger_auto_schema(
		operation_summary="Initiate/Update Employee Report Record ",
		responses={
			'200': SucessResponseSerializer,
			'422': ErrorSerializer,
			'500': SystemErrorSerializer})
	def post(self, request, *args, **kwargs):
		request_dict = request.data.copy()
		form = ReportForm(request_dict)
		if form.is_valid():
			try:
				if 'id' in request_dict:

					my_report= Report.objects.get(id=request_dict["id"], user_id=request_dict["user_id"])
					my_report.title = request_dict["title"]
					my_report.priority = request_dict["priority"]
					my_report.solved = bool(request_dict["solved"])
					my_report.description = request_dict["description"]
					my_report.save()
					message = 'updated'
					my_report, created = Report.objects.update_or_create(id=request_dict["id"],
																	   user_id=request_dict["user_id"],
																	   defaults={"title": request_dict["title"],
																				 "priority": request_dict["priority"],
																				 "solved": bool(request_dict["solved"]),
																				 "description": request_dict[
																					 "description"]})
				else:
					my_report = Report.objects.create(user_id=request_dict["user_id"], title=request_dict["title"],
										  priority = request_dict["priority"], solved = bool(request_dict["solved"]),
										  description = request_dict["description"])
					message = 'created'

				return Response({"detail": "Report with id {} connected to user {} was {}.".
								format(my_report.id,form.my_user.username, message)}, status=200,
								content_type="application/json")
			except Exception:
				logger.critical(traceback.format_exc())
				return Response({"detail": "Error in api: {}".format(traceback.format_exc())}, status=500, content_type="application/json")
		else:
			logger.error(process_general_form_errors(json.loads(form.errors.as_json())))
			return Response(process_general_form_errors(json.loads(form.errors.as_json())),
							content_type="application/json", status=422)


#
# API 3 Querying of the database in order to retrieve reports paginated by 10
#
class FetchReportsApiView(GenericAPIView):
	""" Querying of the database in order to retrieve reports. If you need to filter results you may user username,
	priority or both. Results are paginated by 10."""
	permission_classes = (IsAuthenticated,)

	@swagger_auto_schema(
		query_serializer=FetchReportsSerializer,
		operation_summary="Retrieve Reports Query",
		responses={
			'200': FetchReportsResponseSerializer,
			'422': ErrorSerializer,
			'500': SystemErrorSerializer})

	def get(self, request, *args, **kwargs):
		request_dict = request.GET.copy()
		form = FetchReportForm(request_dict)

		if form.is_valid():
			try:
				filter_components = {}
				if 'username' in request_dict:
					filter_components.update({"user__username": request_dict['username']})
				if 'priority' in request_dict:
					filter_components.update({"priority": request_dict['priority']})

				my_queryset = Report.objects.filter(**filter_components).\
					values("id", "user__id", "user__username", "priority", "title", "description", "solved")

				page = request.GET.get("page", 1)
				p = Paginator(my_queryset, 10)
				response_dict = {"body": list(p.page(page).object_list),
								 "footer": {"page": page,
											"total_pages": p.num_pages}}

				return Response(response_dict, status=200,
								content_type="application/json")
			except Exception:
				logger.critical(traceback.format_exc())
				return Response({"detail": "Error in api: {}".format(traceback.format_exc())}, status=500, content_type="application/json")

		else:
			logger.error(process_general_form_errors(json.loads(form.errors.as_json())))
			return Response(process_general_form_errors(json.loads(form.errors.as_json())),
							content_type="application/json", status=422)


class HomePage(LoginRequiredMixin, TemplateView):

	def get(self, request, *args, **kwargs):
		return render(
			request,
			'rootapp/home.html',
		)


class LoginAdminView(LoginView):

	def post(self, request, *args, **kwargs):

		user_dict = {
			'username': request.POST.get('username')
		}

		try:
			user = User.objects.get(username=user_dict['username'])
		except User.DoesNotExist:
			logger.error("Login user does not exist")
			return super().post(request)
		if not user.is_staff:
			messages.error(request, 'Please enter a correct username and password. Note that both'
									'fields may be case-sensitive.')
			return redirect('new_login')

		return super().post(request)


@permission_classes((IsAuthenticated,))
def direct_auth_logout(request):
	logout(request)
	return render(request, 'registration/logged_out.html')


class Logs(LoginRequiredMixin, TemplateView):

	def get(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return HttpResponse(status=401)
		log_data = openLog()
		lines = len(log_data.index)
		logsdict = {"logdata": re.sub('\s+\n', '\n', log_data.tail(lines)[0].to_string(index=True))}
		return render(request, 'rootapp/logs.html',logsdict)

	def readlog(request, *args, **kwargs):
		if not request.user.is_staff:
			return HttpResponse(status=401)
		qvars = request.GET
		logger.debug("Query variables: {}".format(qvars))
		try:
			log = openLog()
			# result = json.dumps({'start': log.index.start, 'stop': log.index.stop, 'log': log[0].to_string(index=True)})
			result = json.dumps({'log': re.sub('\s+\n', '\n', log[0].to_string(index=True))})
			return HttpResponse(result, content_type="application/json")
		# except FileNotFoundError:
		except Exception as e:
			logger.error("Error in Class logs: {}".format(e))
			if qvars.get('download'):
				response = HttpResponse("", content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename={0}'.format(qvars.get('log'))
				return response
			result = json.dumps({'start': 0, 'stop': 0, 'log': "Empty Log File"})
			return HttpResponse(result, content_type="application/json")

def openLog():
	try:
		pd.set_option('display.max_colwidth', 0)
		filepath = settings.LOG_PATH
		data = pd.read_csv(filepath, sep='r\n', engine='python', header=None, quoting=csv.QUOTE_NONE)
		print("hahahahaha")
		print(data)
		return data
	except Exception as e:
		logger.error("Error in def Openlog: {}".format(e))


