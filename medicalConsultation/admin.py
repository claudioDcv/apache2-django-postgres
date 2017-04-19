from django.contrib import admin
from .models import Patient, DogBreed, DogColor, Veterinarian, MedicalConsultation


class DogColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')


class DogBreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


class MedicalConsultationAdmin(admin.ModelAdmin):
    # fields = ( 'image_tag', )
    # readonly_fields = ('first_image_tag','second_image_tag','third_party')
    list_display = ('first_image_tag','second_image_tag','third_image_tag','title')


class PatientAdmin(admin.ModelAdmin):
    # fields = ( 'image_tag', )
    readonly_fields = ('image_tag',)
    list_display = ('image_tag','name','create_by_info','dog_breed', 'primary_color', 'second_color', 'height_info')

# Register your models here.
admin.site.register(Patient, PatientAdmin)
admin.site.register(DogBreed, DogBreedAdmin)
admin.site.register(DogColor, DogColorAdmin)
admin.site.register(Veterinarian)
admin.site.register(MedicalConsultation,MedicalConsultationAdmin)
# admin.site.register(DogSecondColor)
