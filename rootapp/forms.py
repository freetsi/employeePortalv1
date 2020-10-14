from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import get_default_password_validators, validate_password
from django.core.validators import RegexValidator
from rootapp import models
from rootapp.models import Department, Report
from rootapp.serializers import get_priotities, get_report_title

alphanumeric_symbols = RegexValidator(r'^[\w\$\d-]*$')
numeric = RegexValidator(r'^[\d]*$')


class EmployeeForm(forms.Form):
	username = forms.CharField(required=True, validators=[alphanumeric_symbols])
	email = forms.EmailField(required=True)
	gender = forms.CharField(required=True)
	title = forms.CharField(required=True)
	firstName = forms.CharField(required=True)
	lastName = forms.CharField(required=True)
	fatherName = forms.CharField(required=True)
	department = forms.CharField(required=False)
	birthDate = forms.DateField(required=False, input_formats=['%d/%m/%Y'])
	phone = forms.CharField(required=False, validators=[numeric])
	mobile = forms.CharField(required=False, validators=[numeric])
	address = forms.CharField(required=False)
	postcode = forms.CharField(required=False)
	password = forms.CharField(widget=forms.PasswordInput(), required=False)

	def __init__(self, *args, **kwargs):
		super(EmployeeForm, self).__init__(*args, **kwargs)
		self.my_dep = None

	def clean(self):
		if self.errors:
			return super(EmployeeForm, self)

		username = self.data.get("username")
		email = self.data.get("email")
		gender = self.data.get("gender")

		validation_error_list = []

		# STEP 1
		# Validate parameters
		if gender not in ['male', 'female']:
			validation_error_list.append(forms.ValidationError("Employee Gender {} is not acceptable."
															   " It must be either male/ female".format(gender),
															   code='Invalid gender'))
		if self.data.get("department") not in Department.objects.values_list('name', flat=True):
			validation_error_list.append(forms.ValidationError("Report Priority {} is not acceptable."
															   " It must one of {}".format(priority,get_priotities()),
															   code='Invalid deparment'))

		if not any(self.data.get("title") == e[0] for e in models.TITLE_CHOICES):
			validation_error_list.append(forms.ValidationError("Employee Title {} is not acceptable. "
															   "It must either be entry, junior, mid, senior or manager".format(self.data.get("title")),
															   code='Invalid title'))
		my_user=None
		try:
			my_user = User.objects.get(username = username)
		except User.DoesNotExist:
			# Do nothing since I will create him
			pass
		if not my_user and not self.data.get("password"):
			validation_error_list.append(forms.ValidationError("You must provide a password when creating a new user",
															   code='Required Password'))
		if self.data.get("password"):
			try:
				validators = get_default_password_validators()
				validate_password(self.data.get("password"),User,validators)
			except forms.ValidationError as error:
				self.add_error('password', error)

		if validation_error_list:
			raise forms.ValidationError(validation_error_list)

		self.my_dep = Department.objects.get(name=self.data.get("department"))

class ReportForm(forms.Form):
	title = forms.CharField(required=True),
	description = forms.CharField(required=True)
	user_id = forms.IntegerField(required=True)
	id = forms.IntegerField(required=False)
	priority = forms.CharField(required=True),
	solved = forms.CharField(required=False)

	def __init__(self, *args, **kwargs):
		super(ReportForm, self).__init__(*args, **kwargs)
		self.my_user = None

	def clean(self):
		if self.errors:
			return super(ReportForm, self)

		title = self.data.get("title")
		user_id = self.data.get("user_id")
		priority = self.data.get("priority")
		id = int(self.data.get("id", 0))

		validation_error_list = []

		# Check if priority is in the right form
		if priority not in get_priotities():
			validation_error_list.append(forms.ValidationError("Report Priority {} is not acceptable."
															   " It must one of {}".format(priority,get_priotities()),
															   code='Invalid priority'))
		# Check if title is in the right form
		if title not in get_report_title():
			validation_error_list.append(forms.ValidationError("Report title {} is not acceptable. It must"
															   "be one of {}".format(title,get_report_title()),
															   code='Invalid report'))

		# Check if user exists
		try:
			self.my_user = User.objects.get(id = user_id)
		except User.DoesNotExist:
			validation_error_list.append(forms.ValidationError("User with id {} is not in DB".format(user_id),
															   code='Invalid user id'))

		# In case of not null id (update a report) check that this report exists
		if id != 0:
			try:
				my_rep = Report.objects.get(id=id, user = self.my_user)
			except Report.DoesNotExist:
				validation_error_list.append(forms.ValidationError("Report with id {} for user {} is not in DB.".format(id, self.my_user.id)
																   + " If you need to create a new report don't provide an id",
																   code='Invalid report id'))

		# Check if solved is true or talse
		if self.data.get("solved") and self.data.get("solved") != '':
			if self.data.get("solved").upper() not in ['TRUE', 'FALSE']:
				validation_error_list.append(forms.ValidationError("Solved Variable must be either true or false",
																   code='Invalid solved flag'))
		if validation_error_list:
			raise forms.ValidationError(validation_error_list)


class FetchReportForm(forms.Form):
	username = forms.CharField(required=False)
	priority = forms.CharField(required=False)
	page = forms.IntegerField(required=False)

	def clean(self):
		username = self.data.get("username")
		priority = self.data.get("priority")

		validation_error_list = []

		# Check if user exists
		if username:
			try:
				my_user = User.objects.get(username=username)
			except User.DoesNotExist:
				validation_error_list.append(forms.ValidationError("User with username {} is not in DB".format(username),
																   code='Invalid user id'))
		if priority:
			# Check if priority is high/low
			if priority not in get_priotities():
				validation_error_list.append(forms.ValidationError("Report Priority {} is not acceptable."
																   " It must one of {}".format(priority,get_priotities()),
																   code='Invalid priority'))
		if validation_error_list:
			raise forms.ValidationError(validation_error_list)


