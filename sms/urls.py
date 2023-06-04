from django.contrib import admin
from django.urls import path

from sms.views import IndexPageView, SMSView

urlpatterns = [
    path('', IndexPageView.as_view(), name='sms-view'),
    path('sms/<str:key>', SMSView.as_view(), name='sms-read-view'),
]
