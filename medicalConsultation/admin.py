from django.contrib import admin
from .models import Patient, DogBreed, DogColor


class DogColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')


class DogBreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('name','create_by_info','dog_breed', 'primary_color', 'second_color', 'height_info')

# Register your models here.
admin.site.register(Patient, PatientAdmin)
admin.site.register(DogBreed, DogBreedAdmin)
admin.site.register(DogColor, DogColorAdmin)
# admin.site.register(DogSecondColor)
