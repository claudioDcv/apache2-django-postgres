from django.views.generic import ListView
# from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from medicalConsultation.forms import AnimalBreedForm
from medicalConsultation.models import AnimalBreed
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from vetadminproject.utils import ctm_msg


@method_decorator(login_required, name='dispatch')
class AnimalBreedNew(CreateView):
    template_name = 'patient/animal_breed_new.html'
    form_class = AnimalBreedForm
    success_url = '/consulta/animal-breed/list/'

    # def form_valid(self, form):
    #     # import ipdb; ipdb.set_trace()
    #     # self.object = form.save(commit=False)
    #     # self.object.name = form.cleaned_data['name']
    #     # self.object.animal_type = form.cleaned_data['animal_type']
    #     try:
    #         self.object.save()
    #         messages.add_message(
    #             self.request,
    #             messages.SUCCESS,
    #             ctm_msg('create:ok').format(self.object.name))
    #     except Exception as e:
    #         pass
    #     return HttpResponseRedirect(self.get_success_url())


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
