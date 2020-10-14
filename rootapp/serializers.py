from rest_framework import serializers

from rootapp import models


def get_titles():
	title_list = []
	for e in models.TITLE_CHOICES:
		if e[0] != '':
			title_list.append(e[0])
	return title_list


class EmployeeApiSerializer(serializers.Serializer):
	username = serializers.CharField(required=True)
	email = serializers.CharField(required=True)
	gender = serializers.CharField(required=True,
								   help_text="Only 'female' / 'male' values are allowed")
	title = serializers.CharField(required=True,
								  help_text="Only {} values are allowed".format(get_titles()))
	firstName = serializers.CharField(required=True)
	lastName = serializers.CharField(required=True)
	fatherName = serializers.CharField(required=True)
	department = serializers.CharField(required=True,
									   help_text="'Name' field from Department Model")
	birthDate = serializers.CharField(required=False,
									  help_text="In 'dd/mm/yyyy' format")
	phone = serializers.CharField(required=False)
	mobile = serializers.CharField(required=False)
	address = serializers.CharField(required=False)
	postcode = serializers.CharField(required=False)
	password = serializers.CharField(required=False)

	class Meta:
		ref_name =None


def get_priotities():
	priority_list = []
	for e in models.PRIORITY_CHOICES:
		if e[0] != '':
			priority_list.append(e[0])
	return priority_list

def get_report_title():
	report_title_list = []
	for e in models.REPORT_TITLES_CHOICES:
		if e[0] != '':
			report_title_list.append(e[0])
	return report_title_list


class ReportApiSerializer(serializers.Serializer):
	title = serializers.CharField(required=True,
								  help_text="Only {} values are allowed".format(get_report_title()))
	description = serializers.CharField(required=True)
	user_id = serializers.IntegerField(required=True)
	id = serializers.IntegerField(required=False,
									help_text = "If you need to create a new report don't provide an id")
	priority = serializers.CharField(required=True,
								  help_text="Only {} values are allowed".format(get_priotities()))
	solved = serializers.BooleanField(default=False)

	class Meta:
		ref_name =None

	def get_title(self,obj):
		return obj.get_gender_display()


class FetchReportsSerializer(serializers.Serializer):
	username = serializers.CharField(required=False)
	priority = serializers.CharField(required=False,
									 help_text="Only {} values are allowed".format(get_priotities()))
	page = serializers.IntegerField(required=False,
									help_text = "If you don't provide one it defaults to page 1")

	class Meta:
		ref_name =None


class FooterSerializer(serializers.Serializer):
	page = serializers.IntegerField(required=True)
	total_pages = serializers.IntegerField(required=True)

	class Meta:
		ref_name =None


class FetchReportsResponseSerializer(serializers.Serializer):
	body = ReportApiSerializer(source='*', many=True)
	footer =FooterSerializer(source='*', many=False)

	class Meta:
		ref_name =None


class SucessResponseSerializer(serializers.Serializer):
	detail = serializers.CharField(required=True)

	class Meta:
		ref_name =None


class ErrorDetailsSerializer(serializers.Serializer):
	title = serializers.CharField(required=True)
	descr = serializers.CharField(required=True)

	class Meta:
		ref_name =None


class ErrorSerializer(serializers.Serializer):
	error = ErrorDetailsSerializer(source='*', many=True)

	class Meta:
		ref_name =None


class SystemErrorSerializer(serializers.Serializer):
	detail = serializers.CharField(required=True)

	class Meta:
		ref_name =None