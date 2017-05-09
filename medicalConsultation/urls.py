from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.PatientList.as_view(), name='patient-list'),
    url(r'^(?P<pk>\d+)/$',
        views.PatientDetail.as_view(), name='patient-detail'),
    url(r'^patient/new/$',
        views.PatientNew.as_view(), name='patient-new'),
    url(r'^control-detail/(?P<pk>\d+)/$',
        views.ControlDetail.as_view(), name='medicalconsultation-detail'),
    url(r'^animal-type/new/$',
        # Animal Type
        views.AnimalTypeNew.as_view(), name='animalType-new'),
    url(r'^animal-type/list/$',
        views.AnimalTypeList.as_view(), name='animalType-list'),
    url(r'^animal-type/delete/(?P<pk>\d+)/$',
        views.AnimalTypeDelete.as_view(), name='animalType-delete'),
    url(r'^animal-type/(?P<pk>\d+)/$',
        views.AnimalTypeEdit.as_view(), name='animalType-edit'),
    url(r'^json-animal-type/$',
        views.JsonAnimalType.as_view(), name='json-animalType-list'),
    url(r'^json-auditor/$',
        views.JsonAuditor.as_view(), name='json-auditor-list'),
    # Animal Breed
    url(r'^animal-breed/new/$',
        views.AnimalBreedNew.as_view(), name='animalBreed-new'),
    url(r'^animal-breed/list/$',
        views.AnimalBreedList.as_view(), name='animalBreed-list'),
    url(r'^animal-breed/delete/(?P<pk>\d+)/$',
        views.AnimalBreedDelete.as_view(), name='animalBreed-delete'),
    url(r'^animal-breed/(?P<pk>\d+)/$',
        views.AnimalBreedEdit.as_view(), name='animalBreed-edit'),
]
