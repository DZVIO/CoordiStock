from django.db import models
from .choices import *
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.validators import MinLengthValidator

####################################################################################################

class Terminal(models.Model):
    terminal = models.CharField(max_length=50, verbose_name="Terminal", unique=True)
    ciudad = models.CharField(max_length=50, choices=[(ciudad, ciudad) for ciudad in ciudades_colombia], default='Bogotá ()', verbose_name="Ciudad")
    direccion = models.CharField(max_length=50, verbose_name="Dirección")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    def __str__(self):
        return f"{self.terminal}"

    class Meta:
        verbose_name= "terminal"
        verbose_name_plural ='terminales'
        db_table ='Terminal'    

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
        return f"{self.proveedor}: {self.nit}"

    class Meta:
        verbose_name= "proveedor"
        verbose_name_plural ='proveedores'
        db_table ='Proveedor'

####################################################################################################

class Area(models.Model):
    area = models.CharField(max_length=50, verbose_name="Area", unique=True)    
    estado = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return f"{self.area}"

    class Meta:
        verbose_name= "area"
        verbose_name_plural ='areas'
        db_table ='Area'

####################################################################################################

class Agente(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = 'CC', 'Cédula de Ciudadanía'
        TI = 'TI', 'Tarjeta de Identidad'
        CE = 'CE', 'Cédula de Extranjería'
        RC = 'RC', 'Registro Civil'
        PSP = 'PSP', 'Pasaporte'

    def validar_email(value):
        value = "foo.bar@baz.qux"
        try:
            validate_email(value)
        except ValidationError:
            raise ValidationError("Correo rechazado")  
        
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    codigo = models.PositiveIntegerField(verbose_name="Código", unique=True)
    tipo_documento = models.CharField(max_length=3, choices=TipoDocumento.choices, default=TipoDocumento.CC, verbose_name="Tipo de documento")
    numero_documento = models.PositiveIntegerField(verbose_name="Número de documento", unique=True)
    email = models.EmailField(max_length=50, verbose_name="Email", validators=[validate_email])
    pais_telefono = models.CharField(max_length=50, choices=[(pais, pais) for pais in codigos_telefonicos_paises], default='Colombia (+57)', verbose_name="Prefijo telefónico")
    telefono = models.PositiveIntegerField(verbose_name="Teléfono")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    id_area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name="Area")

    def __str__(self):
        return f"{self.nombre}: {self.codigo} - {self.id_area}"
    
    class Meta:
        verbose_name= "agente"
        verbose_name_plural ='agentes'
        db_table ='Agente'

####################################################################################################

class Factura(models.Model):
    o_compra = models.PositiveIntegerField(verbose_name="Orden de compra", unique=True)
    n_factura = models.CharField(max_length=50, verbose_name="N. de factura", unique=True)
    pdf_factura = models.FileField(upload_to='facturas_pdfs/', verbose_name="PDF de la factura", null=True, blank=True)
    in_garantia = models.DateTimeField(verbose_name="Fecha de inicio de garantía")
    fin_garantia = models.DateTimeField(verbose_name="Fecha de fin de garantía")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, verbose_name="Proveedor")

    def __str__(self):
        return f"{self.o_compra}: {self.n_factura}"

    class Meta:
        verbose_name= "factura"
        verbose_name_plural ='facturas'
        db_table ='Factura'

####################################################################################################

class Activo(models.Model):
    class categorias(models.TextChoices):
        PC = 'PC', 'PC'
        LAPTOP = 'Laptop', 'Laptop'
        PERIFERICOS = 'Perifericos', 'Perifericos'

    fecha_reg = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    renting = models.BooleanField(default=False, verbose_name="Renting")
    activo = models.PositiveIntegerField(verbose_name="Activo", unique=True)
    categoria = models.CharField(max_length=50, choices=categorias.choices, default=categorias.PC, verbose_name="Categoría")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    n_serie = models.CharField(max_length=50, verbose_name="N. de serie", unique=True)
    observaciones = models.CharField(max_length=300, verbose_name="Observaciones")
    garantia = models.BooleanField(default=True, verbose_name="Garantía")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    id_terminal = models.ForeignKey(Terminal, on_delete=models.PROTECT, verbose_name="Terminal")
    id_marca = models.ForeignKey(Marca, on_delete=models.PROTECT, verbose_name="Marca")
    id_agente = models.ForeignKey(Agente, on_delete=models.PROTECT, verbose_name="Agente")
    id_area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name="Area")
    id_factura = models.ForeignKey(Factura, on_delete=models.PROTECT, verbose_name="Factura")

    def __str__(self):
        return f"{self.activo}"

    class Meta:
        verbose_name= "activo"
        verbose_name_plural ='activos'
        db_table ='Activo'

####################################################################################################

class Administrador(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = 'CC', 'Cédula de Ciudadanía'
        CE = 'CE', 'Cédula de Extranjería'
        PSP = 'PSP', 'Pasaporte'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrador')
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    tipo_documento = models.CharField(max_length=3, choices=TipoDocumento.choices, default=TipoDocumento.CC, verbose_name="Tipo de documento")
    numero_documento = models.PositiveIntegerField(verbose_name="Número de documento")
    telefono = models.PositiveIntegerField(verbose_name="Teléfono")
    contrasena = models.CharField(max_length=128, validators=[MinLengthValidator(8)], verbose_name="Contraseña")
    conf_contrasena = models.CharField(max_length=128, verbose_name="Confirmación de contraseña", default="")

    def clean(self):
        super().clean()
        if self.contrasena != self.conf_contrasena:
            raise ValidationError({"conf_contrasena": "Las contraseñas no coinciden"})

    def save(self, *args, **kwargs):
        if not self.pk or 'user' not in kwargs:
            user, created = User.objects.get_or_create(username=self.user.username)
        else:
            user = self.user

        if self.contrasena:
            user.set_password(self.contrasena)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        db_table = 'Administrador'

@receiver(post_delete, sender=Administrador)
def eliminar_usuario_relacionado(sender, instance, **kwargs):
    user = instance.user
    if user:
        user.delete()

####################################################################################################

class Operador(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = 'CC', 'Cédula de Ciudadanía'
        TI = 'TI', 'Tarjeta de Identidad'
        CE = 'CE', 'Cédula de Extranjería'
        PSP = 'PSP', 'Pasaporte'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operador')
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    tipo_documento = models.CharField(max_length=3, choices=TipoDocumento.choices, default=TipoDocumento.CC, verbose_name="Tipo de documento")
    numero_documento = models.PositiveIntegerField(verbose_name="Número de documento", unique=True)
    telefono = models.PositiveIntegerField(verbose_name="Teléfono")
    contrasena = models.CharField(max_length=128, validators=[MinLengthValidator(8)], verbose_name="Contraseña")
    conf_contrasena = models.CharField(max_length=128, verbose_name="Confirmación de contraseña", default="")

    def clean(self):
        super().clean()
        if self.contrasena != self.conf_contrasena:
            raise ValidationError({"conf_contrasena": "Las contraseñas no coinciden"})

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"
        db_table = 'Operador'

@receiver(post_delete, sender=Operador)
def eliminar_usuario_relacionado(sender, instance, **kwargs):
    user = instance.user
    if user:
        user.delete()

###################################################################################################

class Movimiento(models.Model):
    fecha_mov = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de movimiento")
    motivo = models.CharField(max_length=50, verbose_name="Motivo")
    ubicacion = models.CharField(max_length=50, verbose_name="Ubicación")

    def __str__(self):
        return f"{self.fecha_mov}"

    class Meta:
        verbose_name= "movimiento"
        verbose_name_plural ='movimientos'
        db_table ='Movimiento'

####################################################################################################

class Detalle_movimiento(models.Model):
    class t_m(models.TextChoices):
        MANTENIMIENTO = 'Mantenimiento', 'Mantenimiento'
        PRESTAMO = 'Prestamo', 'Prestamo'
        ASIGNACION = 'Asignacion', 'Asignacion'
        TRASLADO = 'Traslado', 'Traslado'
        D_FINAL = 'Dispocicion final', 'Dispocicion final'

    tipo_mov = models.CharField(max_length=50, choices=t_m.choices, default=t_m.PRESTAMO, verbose_name="Tipo de movimiento")
    id_activo = models.ForeignKey(Activo, on_delete=models.PROTECT, verbose_name="Activo")
    id_movimiento = models.ForeignKey(Movimiento, on_delete=models.PROTECT, verbose_name="Movimiento")
    id_agente = models.ForeignKey(Agente, on_delete=models.PROTECT, verbose_name="Agente")

    def __str__(self):
        return f"{self.id_movimiento}"

    class Meta:
        verbose_name= "detalle_movimiento"
        verbose_name_plural ='detalle_movimientos'
        db_table ='Detalle_movimiento'