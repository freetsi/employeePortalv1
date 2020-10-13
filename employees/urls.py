"""employees URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, renderers
from rest_framework.schemas import get_schema_view as restframework_get_schema_view

from employees import settings
from rootapp import views
from rootapp.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Employee API",
        default_version='v1',
        description="Web Services API reference",),
    # patterns=api_urls + token_urls,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rootapp.urls')),
    path('api/tester/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/documentation/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('accounts/login/', views.LoginAdminView.as_view(), name='new_login'),
    path('accounts/logout/', views.direct_auth_logout, name='logout'),
    path('console/', views.HomePage.as_view(), name="home"),
    path('', RedirectView.as_view(url='/console', permanent=True), name='home'),
    # path('api/', include('rootapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                   staticfiles_urlpatterns()
