from django.contrib import admin
from .models import MeasuringUnit, MedicalEquipment, Medicine


class MedicalEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'stock')


class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'stock')


# Register your models here.
admin.site.register(MeasuringUnit)
admin.site.register(MedicalEquipment, MedicalEquipmentAdmin)
admin.site.register(Medicine, MedicineAdmin)
