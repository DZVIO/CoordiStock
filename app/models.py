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
    terminal = models.CharField(max_length=50, choices=[(ciudad, ciudad) for ciudad in ciudades_colombia], default='Bogotá ()', verbose_name="Ciudad")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    direccion = models.CharField(max_length=50, verbose_name="Dirección")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    def __str__(self):
        return f"{self.terminal} - {self.nombre} - {self.direccion}"

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
    class Modalidad(models.TextChoices):
        PR = 'PR', 'Presencial'
        RM = 'RM', 'Remoto'
        ES = 'ES', 'En sitio'

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
    telefono = models.PositiveIntegerField(verbose_name="Teléfono")
    id_area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name="Area")
    id_terminal = models.ForeignKey(Terminal, on_delete=models.PROTECT, verbose_name="Terminal")
    modalidad = models.CharField(max_length=2, choices=Modalidad.choices, default=Modalidad.PR, verbose_name="Modalidad")
    ubicacion = models.CharField(max_length=50, verbose_name="Ubicación")
    estado = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return f"{self.nombre}: {self.codigo} - {self.id_area}"
    
    class Meta:
        verbose_name= "agente"
        verbose_name_plural ='agentes'
        db_table ='Agente'

####################################################################################################

class Activo(models.Model):
    class categorias(models.TextChoices):
        PC = 'PC', 'PC'
        LAPTOP = 'Laptop', 'Laptop'
        MONITOR = 'Monitor', 'Monitor'
        DIADEMA = 'Diadema', 'Diadema'
        TECLADO = 'Teclado', 'Teclado'
        MOUSE = 'Mouse', 'Mouse'
        BASE_R = 'Base Refrigerante', 'Base Refrigerante'

    fecha_reg = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    tipo = models.BooleanField(default=True, verbose_name="Tipo")
    categoria = models.CharField(max_length=50, choices=categorias.choices, verbose_name="Categoría")
    id_marca = models.ForeignKey(Marca, on_delete=models.PROTECT, verbose_name="Marca")
    activo = models.PositiveIntegerField(verbose_name="Activo", unique=True, blank=True, null=True)
    renting = models.BooleanField(default=False, verbose_name="Renting")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    n_serie = models.CharField(max_length=50, verbose_name="N. de serie", unique=True)
    disponibilidad = models.BooleanField(default=True, verbose_name="Disponibilidad")
    estado = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return f"{self.activo}"
    def clean(self):
        if self.categoria == self.categorias.MONITOR and self.renting:
            raise ValidationError({'renting': 'Las pantallas no pueden ser de renting.'})

        # if self.categoria == self.categorias.MONITOR and self.nomenclatura:
        #     raise ValidationError({'nomenclatura': 'Las pantallas no requieren una nomenclatura.'})

        # if self.renting and self.id_area.area.lower() not in ["call center", "t.i"]:
        #     raise ValidationError({'id_area': 'Los equipos en renting solo pueden asignarse a las áreas de Call Center o T.I.'})

        # if self.categoria in [self.categorias.PC, self.categorias.LAPTOP] and not self.nomenclatura:
        #     raise ValidationError({'nomenclatura': 'Las laptops y PCs requieren una nomenclatura obligatoria.'})

        perifericos = [
            self.categorias.DIADEMA, 
            self.categorias.TECLADO, 
            self.categorias.MOUSE, 
            self.categorias.BASE_R, 
        ]

        if self.categoria not in perifericos:
            activo_str = str(self.activo)
            if self.renting and len(activo_str) != 8:
                raise ValidationError({'activo': 'Si el equipo es de renting, el activo debe tener 8 dígitos.'})
            elif not self.renting and len(activo_str) != 5:
                raise ValidationError({'activo': 'Si el equipo NO es de renting, el activo debe tener 5 dígitos.'})

        # if self.renting and self.id_agente.id_area.area.lower() not in ["call center", "t.i"]:
        #     raise ValidationError({'id_agente': 'Un equipo en renting solo puede asignarse a un agente de Call Center o T.I.'})

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
    class t_m(models.TextChoices):
        ASIGNACION = 'Asignación', 'Asignación'
        MANTENIMIENTO = 'Mantenimiento', 'Mantenimiento'
        PRESTAMO = 'Préstamo', 'Préstamo'
        TRASLADO = 'Traslado', 'Traslado'
        D_FINAL = 'Disposición final', 'Disposición final'

    fecha_mov = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de movimiento")
    tipo_mov = models.CharField(max_length=50, choices=t_m.choices, default=t_m.PRESTAMO, verbose_name="Tipo de movimiento")
    id_terminal = models.ForeignKey(Terminal, on_delete=models.PROTECT, verbose_name="Terminal")

    def __str__(self):
        return f"{self.fecha_mov}"

    class Meta:
        verbose_name= "movimiento"
        verbose_name_plural ='movimientos'
        db_table ='Movimiento'

####################################################################################################

class Detalle_movimiento(models.Model):
    id_movimiento = models.ForeignKey(Movimiento, on_delete=models.PROTECT, verbose_name="Movimiento")
    id_activo = models.ForeignKey(Activo, on_delete=models.PROTECT, verbose_name="Activo")
    motivo = models.CharField(max_length=300, verbose_name="Motivo", )
    id_agente = models.ForeignKey(Agente, on_delete=models.PROTECT, verbose_name="Agente")
    nomenclatura = models.CharField(max_length=50, verbose_name="Nomenclatura", blank=True, null=True)
    id_area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name="Area")
    observaciones = models.CharField(max_length=300, verbose_name="Observaciones")

    def __str__(self):
        return f"{self.id_movimiento}"

    class Meta:
        verbose_name= "detalle_movimiento"
        verbose_name_plural ='detalle_movimientos'
        db_table ='Detalle_movimiento'