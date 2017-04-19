from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from PIL import Image



import socket
#
# try:
#     HOSTNAME = 'http://localhost:8000/static/'
# except:
#     HOSTNAME = 'localhost'

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

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

class Patient(models.Model):
    create_by = models.ForeignKey('auth.User', verbose_name="Usuario",)
    dog_breed = models.ForeignKey('DogBreed', verbose_name="Raza",)
    primary_color = models.ForeignKey('DogColor', verbose_name="Color Primario", related_name="primary_color")
    second_color = models.ForeignKey('DogColor', verbose_name="Color Secundario", related_name="second_color")

    first_image = models.ImageField(upload_to='uploads/')

    name = models.CharField(max_length=200, verbose_name="Nombre",)
    height = models.FloatField(verbose_name="Peso",)
    description = models.TextField(verbose_name="Descripción",)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def image_tag(self):
        return u'<style>#result_list .image-thumbnail{width: auto;margin: -8px;height: 27px;}</style><img style="max-height: 300px;max-width: 300px;"class="image-thumbnail" src="/%s" />' % self.first_image
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


    #override to admin
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
        return self.name

    class Meta:
        verbose_name = 'paciente'


# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Patient)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.first_image.delete(False)


class DogBreed(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Nombre",)
    code = models.CharField(max_length=200, unique=True, verbose_name="Código",)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'raza'


class DogColor(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre",)
    code = models.CharField(max_length=100, unique=True, verbose_name="Código",)
    description = models.TextField(verbose_name="Descripción",)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'color'
        verbose_name_plural = 'colores'


class MedicalConsultation(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Titulo",)
    patient = models.ForeignKey('Patient', verbose_name="paciente",)
    veterinarian = models.ForeignKey('Veterinarian', verbose_name="veterinario",)
    description = models.TextField(verbose_name="Descripción",)

    first_image = models.ImageField(upload_to='uploads/')
    second_image = models.ImageField(upload_to='uploads/')
    third_image = models.ImageField(upload_to='uploads/')

    def first_image_tag(self):
        return u'<style>#result_list .image-thumbnail{width: auto;margin: -8px;height: 27px;}</style><img style="max-height: 300px;max-width: 300px;"class="image-thumbnail" src="/%s" />' % self.first_image
    first_image_tag.short_description = 'Image 1'
    first_image_tag.allow_tags = True

    def second_image_tag(self):
        return u'<style>#result_list .image-thumbnail{width: auto;margin: -8px;height: 27px;}</style><img style="max-height: 300px;max-width: 300px;"class="image-thumbnail" src="/%s" />' % self.second_image
    second_image_tag.short_description = 'Image 2'
    second_image_tag.allow_tags = True

    def third_image_tag(self):
        return u'<style>#result_list .image-thumbnail{width: auto;margin: -8px;height: 27px;}</style><img style="max-height: 300px;max-width: 300px;"class="image-thumbnail" src="/%s" />' % self.third_image
    third_image_tag.short_description = 'Image 3'
    third_image_tag.allow_tags = True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'consulta medica'
        verbose_name_plural = 'consultas medicas'
'''
Abigarrado: marcas entremezcladas de diferentes colores sin que predomine ninguno.

Albaricoque: color chabacano.

Albino: blanco, sin pigmentaciones.

Amarillo: como el de la raza Vizla.

Arlequín: pelaje de fondo blanco con manchas negras irregulares; es decir, coloración parchada, como el Gran Danés.

Ascob: cualquier color sólido que no sea negro. Este término se usa regularmente con el Cocker Spaniel.

Atigrado: mezcla de pelo negro en forma de rayas sobre un color más claro, como café o rojo, común en el Bóxer.

Avellana: café cremoso.

Azul: va desde el azul gris pálido hasta el azul acero o azul gris, por ejemplo el Kerry Blue Terrier.

Azul grisáceo o grizzle: también llamado mezclilla como el Weimaraner.

Azul mirlo: es marmoleado azul y gris, combinado con un toque de negro.

Belton: una composición de blanco y pelo de color naranja y azul o hígado, es típico en el Setter inglés.

Bleiz: raya blanca corriendo por el centro de la frente entre los ojos, como el Boston terrier.

Bronce: amarillo dorado.

Café: rojizo profundo.

Caoba: rojo dorado.

Cervato: amarillento pálido.

Cobre: Dorado encendido.

Collar: marca alrededor del cuello, habitualmente es blanca, como la que posee el Collie.

Con anteojos: sombras alrededor de los ojos que se extiende hasta las orejas; el Husky Siberiano entra en esta categoría.

Cortado: un color separado por blanco u otro color.

Champaña: amarillo suave.

Chocolate: café oscuro.

Encendido: color subido.

Ensillado: marca negra sobre la espalda.

Flameado: color llama.

Fuego: rojo encendido.

Golondrino: definidos negro y paja, como el Doberman.

Gris carbonado: puntas del pelo en color negro con el fondo gris.

Hígado: café rojizo oscuro.

Isabela: color amarillo parduzco o bayo claro.

Leonado: por lo regular es rojizo o amarillo claro.

Lila: morado azulado.

Manchado: parches grandes de dos o más colores.

Manteado: una mancha en forma de manta.

Marcado: manchas sobre el cuerpo que pueden ser correctas o incorrectas.

Marcas de lápiz: color delineado.

Marrón: café rojizo.

Máscara: delineada sobre la cara, habitualmente negra.

Matices: diferentes tonalidades.

Moteado: con pecas sobre el cuerpo, característico del Dálmata.

Naranja: amarillo intenso.

Paja: dorado, moreno o pardo.

Pardo: color profuso, generalmente grisáceo.

Particolor: manchando con grandes parches de dos o más colores.

Pincelado: marcas negras sobre un fondo claro.

Plateado: gris plata.

Porcelana: color gris sucio.

Roano: mezcla de pelos blancos sobre una base azul, naranja o limón.

Rubio carbonado: puntas negras sobre un fondo canela.

Sal y pimienta: colores gris oscuro con gris claro o blanco pardo, como el Schnauzer miniatura.

Sepia: café rojizo oscuro.

Tricolor: mezcla de colores negro, blanco y café, distintivos en los Hounds.

'''

'''

A
A
Alano
Alaskan Malamute
American Staffordshire Terrier
American Water Spaniel
Antiguo Pastor Inglés

OKSOKS



B
Basset Azul de Gaseogne
Basset Hound
Basset leonado de Bretaña
Beagle
Bearded Collie
Bichón Maltés
Bobtail
Border Collie
Boston Terrier
Boxer
Bull Terrier
Bulldog Americano
Bulldog Francés
Bulldog Inglés
C
Caniche
Carlino
Chihuahua
Cirneco del Etna
Chow Chow
Cocker Spaniel Americano
Cocker Spaniel Inglés
D
Dálmata
Dobermann
Dogo Alemán
Dogo Argentino
Dogo de Burdeos
F
Finlandés
Fox Terrier de pelo liso
Fox Terrier
Foxhound Americano
Foxhound Inglés
G
Galgo Afgano
Gigante de los Pirineos
Golden Retriever
Gos d'Atura
Gran Danés
H
Husky Siberiano
L
Laika de Siberia Occidental
Laika Ruso-europeo
Labrador Retriever
M
Mastín del Pirineo
Mastin del Tibet
Mastín Español
Mastín Napolitano
P
Pastor Alemán
Pastor Australiano
Pastor Belga
Pastor de Brie
Pastor de los Pirineos de Cara Rosa
Pekinés
Perdiguero Chesapeake Bay
Perdiguero de Drentse
Perdiguero de Pelo lido
Perdiguero de pelo rizado
Perdiguero Portugués
Pitbull
Podenco Ibicenco
Podenco Portugués
presa canario
Presa Mallorquin
R
Rottweiler
Rough Collie
S
Sabueso Español
Sabueso Hélenico
Sabueso Italiano
Sabueso Suizo
Samoyedo
San Bernardo
Scottish Terrier
Setter Irlandés
Shar Pei
Shiba Inu
Siberian Husky
Staffordshire Bull Terrier
T
Teckel
Terranova
Terrier Australiano
Terrier Escocés
Terrier Irlandés
Terrier Japonés
Terrier Negro Ruso
Terrier Norfolk
Terrier Norwich
Y
Yorkshire Terrier

'''
