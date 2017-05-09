from django import forms
from .models import AnimalType, AnimalBreed, Patient
from vetadminproject.utils import code_generate
from django.core.exceptions import ValidationError
from django.db import IntegrityError
# from django.utils.translation import ugettext_lazy as _


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        exclude = ('create_by', 'animal_type')


class AnimalTypeForm(forms.ModelForm):

    class Meta:
        model = AnimalType
        fields = ('name', 'code')

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

    def is_valid(self):
        """
        Returns True if the form has no errors. Otherwise, False. If errors are
        being ignored, returns False.
        """
        return self.is_bound and not self.errors

    def __init__(self, *args, **kwargs):
        super(AnimalTypeForm, self).__init__(*args, **kwargs)
        self.fields.pop('code')

    def clean_name(self):
        clean_dict = self.cleaned_data
        name = clean_dict.get('name')

        try:
            listing = AnimalType.objects.get(code=code_generate(name))
        except Exception as e:
            listing = None

        if listing is not None:
            raise forms.ValidationError(
                "Ya existe Tipo Animal con nombre {}.".format(name))

        if len(name) < 3:
            raise forms.ValidationError(
                "El nombre debe contener mas de tres caracteres")
        return name


class AnimalBreedForm(forms.ModelForm):

    class Meta:
            model = AnimalBreed
            # widgets = {'code': forms.HiddenInput()}
            fields = ('name', 'code', 'animal_type')
            exclude = ['code']

    def __init__(self, *args, **kwargs):
        super(AnimalBreedForm, self).__init__(*args, **kwargs)
        self.fields['animal_type'].empty_label = 'Tipo de Animal'

    def clean(self):
        instance = super(AnimalBreedForm, self).save(commit=False)
        instance.name = self.cleaned_data.get('name')
        instance.animal_type = self.cleaned_data.get('animal_type')
        instance.code = code_generate(instance.name)

        min_size = 3
        if len(instance.name) < min_size:
            raise forms.ValidationError(
                "El nombre debe contener mas de {} caracteres".format(
                    str(min_size-1)))
        else:
            try:
                instance.save()
            except IntegrityError as e:
                raise ValidationError(str(e))

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
