from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from rootapp import views
from rootapp.views import Logs

router = DefaultRouter()
urlpatterns = [
	path('post/employee/', views.EmployeesApiView.as_view(), name='employee'),
	path('post/report/', views.ReportsApiView.as_view(), name='report'),

	# path('questionnaire/', QuestionnaireApiView.as_view()),
	# path('paymentOrder/', PaymentOrderResponseApiView.as_view()),
	# path('investmentChange/', InvestmentChangeApiView.as_view()),
	# path('policyHolderStanding/', PolicyHolderStandingApiView.as_view()),
	# path('redemptionOrder/', RedemptionOrderRequestApiView.as_view()),
	# path('investmentOptions/', InvestmentOptionsRequestApiView.as_view()),
	# url(r'^system_info/', SystemInfo.as_view(), name='sys_info'),
	# url(r'^audit/', 'admin/logentry/', name='audit'),
	url(r'^logs/$', Logs.as_view(), name='logs'),
	url(r'^logs/log/', Logs.readlog, name='readlog'),
]


urlpatterns += router.urls