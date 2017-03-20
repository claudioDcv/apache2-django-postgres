from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PatientList.as_view(), name='patient-list'),
]
