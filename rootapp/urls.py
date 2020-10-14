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
	path('fetch/reports/', views.FetchReportsApiView.as_view(), name='report_fetch'),
	url(r'^logs/$', Logs.as_view(), name='logs'),
	url(r'^logs/log/', Logs.readlog, name='readlog'),
]


urlpatterns += router.urls