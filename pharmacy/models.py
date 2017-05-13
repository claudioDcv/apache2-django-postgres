from django.db import models
# from django.utils import timezone


class MeasuringUnit(models.Model):
    name = models.CharField(
        max_length=200, unique=True, verbose_name="Nombre",)
    code = models.CharField(
        max_length=200, unique=True, verbose_name="Código",)
    acronym = models.CharField(
        max_length=200, unique=True, verbose_name="Acronimo",)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'unidad de medida'
        verbose_name_plural = 'unidades de medida'


class Supplies(models.Model):
    measuring_unit = models.ForeignKey(
        'MeasuringUnit', verbose_name="Unidad de Medida",)
    name = models.CharField(
        max_length=200, unique=True, verbose_name="Nombre",)
    code = models.CharField(
        max_length=200, unique=True, verbose_name="Código",)
    acronym = models.CharField(
        max_length=200, unique=True, verbose_name="Acronimo",)
    stock = models.FloatField(blank=False)


class Medicine(Supplies):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'medicina'
        verbose_name_plural = 'medicinas'


class MedicalEquipment(Supplies):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'equipamiento médico'
        verbose_name_plural = 'equipamientos médicos'
