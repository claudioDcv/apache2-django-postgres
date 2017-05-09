from django.contrib import admin
from .models import Patient, AnimalBreed, AnimalColor, Veterinarian, \
    MedicalConsultation, AnimalType, Auditor


class AnimalColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')


class AnimalBreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


class MedicalConsultationAdmin(admin.ModelAdmin):
    list_display = (
        'first_image_tag', 'second_image_tag', 'third_image_tag', 'title')


class PatientAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)
    list_display = (
        'image_tag', 'name', 'create_by_info', 'animal_breed',
        'primary_color', 'second_color', 'height_info')

    class Media:
        css = {
            "all": ("admin.css",)
        }
# Register your models here.


admin.site.register(Auditor)
admin.site.register(AnimalType)
admin.site.register(Patient, PatientAdmin)
admin.site.register(AnimalBreed, AnimalBreedAdmin)
admin.site.register(AnimalColor, AnimalColorAdmin)
admin.site.register(Veterinarian)
admin.site.register(MedicalConsultation, MedicalConsultationAdmin)
# admin.site.register(DogSecondColor)
