from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from django.core import serializers
from django.db.models import Q
import json
from .forms import AnimalTypeForm, PatientForm, AnimalBreedForm
from .models import Patient, MedicalConsultation, AnimalType, Auditor, \
    AnimalBreed
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from vetadminproject.utils import ctm_msg
import datetime
from vetadminproject.utils import human_text_generate


@method_decorator(login_required, name='dispatch')
class PatientNew(CreateView):
    template_name = 'patient/patient_new.html'
    form_class = PatientForm
    success_url = '/consulta/'
    success_message = 'List successfully saved!!!!'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.create_by = self.request.user
        self.object.animal_type = self.object.animal_breed.animal_type
        try:
            self.object.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Creado con exito'
            )
        except Exception as e:
            pass
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class PatientList(ListView):
    model = Patient
    template_name = 'patient/patient_list.html'


@method_decorator(login_required, name='dispatch')
class PatientDetail(DetailView):
    model = Patient
    template_name = 'patient/patient_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PatientDetail, self).get_context_data(**kwargs)
        context['medicalconsultation'] = MedicalConsultation.objects.filter(
            patient=kwargs['object'].pk
        )
        data = Patient.objects.annotate(
            animal_breeds=Count('name')).order_by('animal_breed')
        context['data'] = serializers.serialize("json", data)
        return context


@method_decorator(login_required, name='dispatch')
class ControlDetail(DetailView):
    model = MedicalConsultation
    template_name = 'patient/control_detail.html'


@method_decorator(login_required, name='dispatch')
class AnimalTypeList(ListView):
    template_name = 'patient/animal_type_list.html'
    paginate_by = 10
    context_object_name = 'animals'

    def get_context_data(self, **kwargs):
        context = super(AnimalTypeList, self).get_context_data(**kwargs)
        context['last_order_by'] = 'id'
        if 'search' in self.request.GET:
            context['search'] = self.request.GET['search']
        if 'order_by' in self.request.GET:
            context['order_by'] = self.request.GET['order_by']
            context['last_order_by'] = self.request.GET['order_by']
        if 'page' in self.request.GET:
            context['page'] = self.request.GET['page']
        return context

    def get_queryset(self):
        objects = AnimalType.objects.all()
        if 'search' in self.request.GET:
            objects = objects.filter(
                    Q(name__icontains=self.request.GET['search']) |
                    Q(code__icontains=self.request.GET['search'])
                )

        if 'order_by' in self.request.GET:
            order_by = self.request.GET['order_by']
            if order_by is not None and order_by != '':
                objects = objects.order_by(order_by)

        return objects

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


@method_decorator(login_required, name='dispatch')
class AnimalTypeEdit(UpdateView):
    template_name = 'patient/animal_type_edit.html'
    model = AnimalType
    fields = ['name']
    success_url = '/consulta/animal-type/list/'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.code = 'perro'
        error = True

        try:
            self.object.save()
        except IntegrityError as e:
            error = False
            self.success_url = '/consulta/animal-type/' \
                + str(self.object.pk) + '/'
            messages.error(
                self.request,
                ctm_msg('update:nok').format(self.object.name)
            )

        if error:
            messages.success(self.request, "Actualizado con exito")

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class AnimalTypeNew(CreateView):
    template_name = 'patient/animal_type_new.html'
    form_class = AnimalTypeForm
    success_url = '/consulta/animal-type/list/'
    success_message = 'List successfully saved!!!!'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Creado con exito'
            )
        except Exception as e:
            pass
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class AnimalTypeDelete(DeleteView):
    model = AnimalType
    template_name = 'patient/animal_type_confirm_delete.html'
    success_url = reverse_lazy('animalType-list')
    success_message = "Eliminación Exitosa"
    is_success = False

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = self.get_success_url()
        try:
            obj = self.object
            self.object.delete()
            messages.success(
                self.request,
                'Tipo de Animal {} eliminado'.format(obj.name))
        except Exception as e:
            messages.error(
                self.request,
                'No se puede eliminar existen elementos dependientes')
        return HttpResponseRedirect(self.success_url)


#############################################################################
#                   AnimalBreed                                             #
#############################################################################

@method_decorator(login_required, name='dispatch')
class AnimalBreedNew(CreateView):
    template_name = 'patient/animal_breed_new.html'
    form_class = AnimalBreedForm
    success_url = '/consulta/animal-breed/list/'

    def form_valid(self, form):
        # import ipdb; ipdb.set_trace()
        self.object = form.save(commit=False)
        # self.object.name = form.cleaned_data['name']
        # self.object.animal_type = form.cleaned_data['animal_type']
        try:
            self.object.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                ctm_msg('create:ok').format(self.object.name))
        except Exception as e:
            pass
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class AnimalBreedDelete(DeleteView):
    model = AnimalBreed
    template_name = 'patient/animal_breed_confirm_delete.html'
    success_url = reverse_lazy('animalBreed-list')
    success_message = "Eliminación Exitosa"
    is_success = False

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = self.get_success_url()
        try:
            obj = self.object
            self.object.delete()
            messages.success(
                self.request,
                'Raza {} eliminado'.format(obj.name))
        except Exception as e:
            messages.error(
                self.request,
                'No se puede eliminar existen elementos dependientes')
        return HttpResponseRedirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class AnimalBreedEdit(UpdateView):
    template_name = 'patient/animal_breed_new.html'
    success_url = '/consulta/animal-breed/list/'
    model = AnimalBreed
    fields = ['name', 'animal_type']

    def form_valid(self, form):
        # import ipdb; ipdb.set_trace()
        self.object = form.save(commit=False)
        # self.object.name = form.cleaned_data['name']
        # self.object.animal_type = form.cleaned_data['animal_type']
        try:
            self.object.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                ctm_msg('create:ok').format(self.object.name))
        except Exception as e:
            messages.error(
                self.request,
                'No se puede eliminar existen elementos dependientes')
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class AnimalBreedList(ListView):
    template_name = 'patient/animal_breed_list.html'
    paginate_by = 10
    context_object_name = 'AnimalBreed'

    def get_context_data(self, **kwargs):
        context = super(AnimalBreedList, self).get_context_data(**kwargs)
        if 'search' in self.request.GET:
            context['search'] = self.request.GET['search']
        return context

    def get_queryset(self):

        if 'search' in self.request.GET:
            objects = AnimalBreed.objects.filter(
                Q(name__icontains=self.request.GET['search']) |
                Q(code__icontains=self.request.GET['search']) |
                Q(animal_type__name__icontains=self.request.GET['search'])
            )
        else:
            objects = AnimalBreed.objects.all()
        return objects


@method_decorator(login_required, name='dispatch')
class JsonAnimalType(ListView):

        def get(self, request):
            animalType = AnimalType.objects.order_by('id').all()
            animalList = []

            if 'q' in self.request.GET:
                animalType = AnimalType.objects.filter(
                    Q(name__icontains=self.request.GET['q']) |
                    Q(code__icontains=self.request.GET['q']))

            for e in animalType:
                print(e.code, e.name, e.id)
                animalList.append({
                    'id': e.id,
                    'value': e.code,
                    'text': e.name,
                })

            obj_select = {
                'total_count': AnimalType.objects.count(),
                'items': animalList,
            }
            return HttpResponse(
                json.dumps(obj_select),
                content_type="application/json"
            )


@method_decorator(login_required, name='dispatch')
class JsonAuditor(ListView):

        def get(self, request):
            animalType = Auditor.objects.filter(
                created_at__gte=datetime.date.today()).order_by('id').all()
            animalList = []

            # if 'q' in self.request.GET:
            #     animalType = AnimalType.objects.filter(
            #         Q(name__icontains=self.request.GET['q']) |
            #         Q(code__icontains=self.request.GET['q']))

            for e in animalType:
                animalList.append({
                    'id': e.id,
                    'tag': human_text_generate(e.tag),
                    'action': e.action,
                    'object': e.content_object._meta.verbose_name,
                })

            obj_select = {
                'total_count': animalType.count(),
                'items': animalList,
            }
            return HttpResponse(
                json.dumps(obj_select),
                content_type="application/json"
            )
# end
