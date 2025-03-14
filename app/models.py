from django.db import models
from .choices import codigos_telefonicos_paises
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.validators import MinLengthValidator

####################################################################################################

class Categoria(models.Model):
    categoria = models.CharField(max_length=50, verbose_name="Categoría", unique=True)
    estado = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return f"{self.categoria}"

    class Meta:
        verbose_name= "categoria"
        verbose_name_plural ='categorias'
        db_table ='Categoria'

####################################################################################################

class Marca(models.Model):
    marca = models.CharField(max_length=50, verbose_name="Marca", unique=True)
    estado = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return f"{self.marca}"

    class Meta:
        verbose_name= "marca"
        verbose_name_plural ='marcas'
        db_table ='Marca'

####################################################################################################

class Proveedor(models.Model):
    proveedor = models.CharField(max_length=50, verbose_name="Proveedor", unique=True)
    nit = models.PositiveIntegerField(verbose_name="NIT", unique=True)
    estado = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return f"{self.marca}"

    class Meta:
        verbose_name= "marca"
        verbose_name_plural ='marcas'
        db_table ='Marca'