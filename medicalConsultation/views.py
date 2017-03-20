from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
import datetime

from .models import Patient, DogBreed

class PatientList(ListView):
    model = Patient
    template_name = 'patient/patient_list.html'
