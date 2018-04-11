"""pushnotify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from .views import IndexView, SendMessage

router = DefaultRouter()
router.register(r'devices', FCMDeviceViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='FCM django web demo')),
    url(r'^', include(router.urls)),
    # url(r'^send_message', send_message, name="send"),
    url(r'^send_message', SendMessage.as_view(), name="send"),
    url(r'^users', IndexView.as_view(), name='home'),
]
