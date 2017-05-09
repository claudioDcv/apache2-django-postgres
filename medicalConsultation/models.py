from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from vetadminproject.utils import code_generate, resize_image
from .decorators import decorator_auditor_save
# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import os


class Auditor(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    action = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag


class VeterinarianManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')
        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.save()
        return account


class Veterinarian(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    tagline = models.CharField(max_length=140, blank=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VeterinarianManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'veterinario'
        verbose_name_plural = 'veterinarios'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name


class AnimalType(models.Model):

    name = models.CharField(
        max_length=200, unique=True, verbose_name="Nombre",)
    code = models.CharField(
        max_length=200, unique=True, verbose_name="Código",)

    def __str__(self):
        return code_generate(self.name)

    class Meta:
        verbose_name = 'tipo de animal'
        verbose_name_plural = 'tipo de animales'

    def delete(self, *args, **kwargs):
        auditor = Auditor(content_object=self, tag=str(self), action='delete')
        super(AnimalType, self).delete(*args, **kwargs)
        auditor.save()

    @decorator_auditor_save
    def save(self, *args, **kwargs):
        self.code = code_generate(self.name)
        object_id = self.id
        super(AnimalType, self).save(*args, **kwargs)
        auditor = None
        if object_id is not None:
            auditor = Auditor(
                content_object=self, tag=str(self), action='update')
        else:
            auditor = Auditor(
                content_object=self, tag=str(self), action='save')
        auditor.save()
        # t.content_object


class Patient(models.Model):
    create_by = models.ForeignKey('auth.User', verbose_name="Usuario",)
    animal_breed = models.ForeignKey('AnimalBreed', verbose_name="Raza",)
    primary_color = models.ForeignKey(
        'AnimalColor',
        verbose_name="Color Primario",
        related_name="primary_color")
    animal_type = models.ForeignKey(
        'AnimalType',
        verbose_name="Tipo de Animal",
        on_delete=models.PROTECT)
    second_color = models.ForeignKey(
        'AnimalColor',
        verbose_name="color secundario",
        related_name="second_color")

    # first_image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    first_image = models.ImageField(upload_to='uploads/')

    name = models.CharField(max_length=200, verbose_name="Nombre",)
    height = models.FloatField(verbose_name="Peso",)
    description = models.TextField(verbose_name="Descripción",)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def image_tag(self):

        try:
            self.first_image.url
        except Exception as e:
            return u'<span></span>'
        return u'<style>#result_list .image-thumbnail{width: auto;margin: -8px;height: 27px;}</style><img style="max-height: 300px;max-width: 300px;"class="image-thumbnail" src="/%s" />' % self.first_image  # noqa: ES01

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def height_info(self):
        return str(self.height) + 'KG'
    height_info.short_description = 'Peso, (KG)'

    def create_by_info(self):
        return self.create_by.username + ' - #' + str(self.create_by.id)
    create_by_info.short_description = 'Creado por'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return code_generate(self.name)

    class Meta:
        verbose_name = 'paciente'

    def delete(self, *args, **kwargs):
        auditor = Auditor(content_object=self, tag=str(self), action='delete')
        try:
            if os.path.isfile(self.first_image.path):
                os.remove(self.first_image.path)
        except Exception as e:
            raise ValueError(e)
        super(Patient, self).delete(*args, **kwargs)
        auditor.save()

    def save(self, *args, **kwargs):

        exist_old = True
        try:
            old_data = Patient.objects.get(id=self.id)
        except Exception as e:
            exist_old = False
        if exist_old:
            pass
            # Delete old image
            # old_data.first_image.delete()

        super(Patient, self).save(*args, **kwargs)
        if exist_old:
            new_data = Patient.objects.get(id=self.id)
            resize_image(new_data.first_image)
            # old_data.first_image.delete()
            if new_data.first_image.path != old_data.first_image.path:
                print(new_data.first_image.path, old_data.first_image.path)
                if os.path.isfile(old_data.first_image.path):
                    os.remove(old_data.first_image.path)
            t = Auditor(content_object=self, tag=str(self), action='update')
            t.save()
        else:
            t = Auditor(content_object=self, tag=str(self), action='save')
            t.save()


class AnimalBreed(models.Model):

    name = models.CharField(
        max_length=200, verbose_name="Nombre",)
    code = models.CharField(
        max_length=200, verbose_name="Código",)
    animal_type = models.ForeignKey(
        'AnimalType', verbose_name="Tipo de Animal")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("code", "animal_type")
        verbose_name = 'raza'

    def save(self, *args, **kwargs):
        self.code = code_generate(self.name)
        object_id = self.id
        super(AnimalBreed, self).save(*args, **kwargs)
        auditor = None
        if object_id is not None:
            auditor = Auditor(
                content_object=self, tag=str(self), action='update')
        else:
            auditor = Auditor(
                content_object=self, tag=str(self), action='save')
        auditor.save()
    # def save(self, *args, **kwargs):
    #     try:
    #         super(AnimalBreed, self).save(*args, **kwargs)
    #     except Exception as e:
    #


class AnimalColor(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Nombre",)
    code = models.CharField(
        max_length=100, unique=True, verbose_name="Código",)
    description = models.TextField(verbose_name="Descripción",)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'color'
        verbose_name_plural = 'colores'


class MedicalConsultation(models.Model):
    title = models.CharField(
        max_length=100, unique=True, verbose_name="Titulo",)
    patient = models.ForeignKey('Patient', verbose_name="paciente",)
    veterinarian = models.ForeignKey(
        'Veterinarian', verbose_name="veterinario",)
    description = models.TextField(verbose_name="Descripción",)

    first_image = models.ImageField(upload_to='uploads/')
    second_image = models.ImageField(upload_to='uploads/')
    third_image = models.ImageField(upload_to='uploads/')

    def first_image_tag(self):
        return u'<img style="max-height: 300px;max-width: 300px;"class="image-thumbnail" src="/%s" />' % self.first_image  # noqa: ES01
    first_image_tag.short_description = 'Image 1'
    first_image_tag.allow_tags = True

    def second_image_tag(self):
        return u'<img style="max-height: 300px;max-width: 300px;"class="image-thumbnail" src="/%s" />' % self.second_image  # noqa: ES01
    second_image_tag.short_description = 'Image 2'
    second_image_tag.allow_tags = True

    def third_image_tag(self):
        return u'<img style="max-height: 300px;max-width: 300px;"class="image-thumbnail" src="/%s" />' % self.third_image  # noqa: ES01
    third_image_tag.short_description = 'Image 3'
    third_image_tag.allow_tags = True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'consulta medica'
        verbose_name_plural = 'consultas medicas'
