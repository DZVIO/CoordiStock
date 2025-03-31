from dataclasses import fields
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget
from django import forms
from django.forms import *
from app.models import *
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Select, NumberInput, EmailInput, PasswordInput

class TerminalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["terminal"].widget.attrs["autofocus"] = True

    class Meta:
        model = Terminal
        fields = "__all__"
        widgets = {
            "terminal": Select(
                attrs={
                    'id': 'terminal',
                    'placeholder': 'Terminal',
                    'class': 'form-control',
                    'name': 'Terminal'
                }
            ),
            "nombre": TextInput(
                attrs={
                    'id': 'nombre',
                    'placeholder': 'Nombre de la terminal',
                    'class': 'form-control',
                    'name': 'nombre'
                }
            ),
            "direccion": TextInput(
                attrs={
                    "placeholder": "Dirección",
                }
            ),
            "estado": Select(
                choices=[(True, "Activo"), (False, "Inactivo")],
                attrs={
                    "placeholder": "Estado de la terminal",
                }
            )
        }

#############################################################################

class MarcaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["marca"].widget.attrs["autofocus"] = True

    class Meta:
        model = Marca
        fields = "__all__"
        widgets = {
            "marca": TextInput(
                attrs={
                    "placeholder": "Marca",
                }
            ),
            "estado": Select(
                choices=[(True, "Activo"), (False, "Inactivo")],
                attrs={
                    "placeholder": "Estado de la marca",
                }
            )
        }

#############################################################################

class AreaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["area"].widget.attrs["autofocus"] = True

    class Meta:
        model = Area
        fields = "__all__"
        widgets = {
            "area": TextInput(
                attrs={
                    "placeholder": "Area",
                }
            ),
            "estado": Select(
                choices=[(True, "Activo"), (False, "Inactivo")],
                attrs={
                    "placeholder": "Estado de la area",
                }
            )
        }

#############################################################################

class AgenteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombre"].widget.attrs["autofocus"] = True

    def validar_num_doc_rep(self):
        numero_documento = self.cleaned_data.get("numero_documento")
        if Agente.objects.filter(numero_documento=numero_documento).exists():
            raise ValidationError("Ya hay un agente registrado con este número de documento.")
        return numero_documento
            
    def validar_email_rep(self):
        email = self.cleaned_data.get("email")
        if Agente.objects.filter(email=email).exists():
            raise ValidationError("Ya hay un agente registrado con este email.")
        return email
    
    class Meta:
        model = Agente
        fields = "__all__"
        widgets = {
            "nombre": TextInput(
                attrs={
                    'id': 'nombre',
                    "placeholder": "Nombre del agente",
                    'class': 'form-control',
                    'name': "nombre",
                }
            ),
            "codigo": NumberInput(
                attrs={
                    'id': 'codigo',
                    "placeholder": "Código del agente",
                    'class': 'form-control',
                    'name': "codigo",
                }
            ),
            "tipo_documento": Select(
                attrs={
                    'id': 'tipo_documento',
                    "placeholder": "Tipo de documento",
                    'class': 'form-control',
                    'name': "tipo_documento",
                }
            ),
            "numero_documento": NumberInput(
                attrs={
                    'id': 'numero_documento',
                    "placeholder": "Número de documento",
                    'class': 'form-control',
                    'name': "numero_documento",
                }
            ),
            "email": EmailInput(
                attrs={
                    'id': 'email',
                    "placeholder": "Email",
                    'class': 'form-control',
                    'name': "email",
                }
            ),
            "telefono": NumberInput(
                attrs={
                    'id': 'telefono',
                    "placeholder": "Teléfono",
                    'class': 'form-control',
                    'name': "telefono",
                }
            ),
            "estado": Select(
                choices=[(True, "Activo"), (False, "Inactivo")],
                attrs={
                    'id': 'estado',
                    "placeholder": "Estado del cliente",
                    'class': 'form-control',
                    'name': "estado",
                },
            )
        }

############################################################################

class ActivoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tipo"].widget.attrs["autofocus"] = True
    class Meta:
        model = Activo
        fields = "__all__"
        exclude = ["fecha_reg"]
        widgets = {
            'tipo': Select(
                choices=[(True, "Activo"), (False, "Periferico")],
            ),
            'categoria': Select(
                attrs={
                    'id': 'categoria',
                    "placeholder": "Categoria",
                    'class': 'form-control',
                    'name': "categoria",
                }
            ),
            'activo': NumberInput(
                attrs={
                    'id': 'activo',
                    "placeholder": "Activo",
                    'class': 'form-control',
                    'name': "activo",
                }   
            ),
            'renting': Select(
                choices=[(True, "Renting"), (False, "No")],
            ),
            'nomenclatura': TextInput(
                attrs={
                    'id': 'nomenclatura',
                    "placeholder": "Nomenclatura",    
                    'class': 'form-control',    
                    'name': "nomenclatura",
                }
            ),
            'modelo': TextInput(
                attrs={
                    'id': 'modelo',
                    "placeholder": "Modelo",
                    'class': 'form-control',
                    'name': "modelo",
                }
            ),
            'n_serie': TextInput(
                attrs={
                    'id': 'n_serie',
                    "placeholder": "Serial",
                    'class': 'form-control',
                    'name': "n_serie",
                }
            ),
            'observaciones': TextInput(
                attrs={
                    'id': 'observaciones',
                    "placeholder": "Observaciones",
                    'class': 'form-control',
                    'name': "observaciones",
                }
            ),
            'estado': Select(
                choices=[(True, "Activo"), (False, "Inactivo")],
                attrs={
                    'id': 'estado',
                    "placeholder": "Estado del activo",
                    'class': 'form-control',
                    'name': "estado",
                }
            )
        }

############################################################################

class AdministradorForm(ModelForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=TextInput(attrs={"placeholder": "Nombre de usuario"})
    )
    email = forms.EmailField(
        label="Email",
        max_length=150,
        widget=EmailInput(attrs={"placeholder": "Correo electrónico"})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=PasswordInput(attrs={"placeholder": "Contraseña"}),
        required=False  
    )
    conf_password = forms.CharField(
        label="Confirmar contraseña",
        widget=PasswordInput(attrs={"placeholder": "Confirmar contraseña"}),
        required=False 
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
        self.fields["username"].widget.attrs["autofocus"] = True

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("conf_password")
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        numero_documento = cleaned_data.get('numero_documento')
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("conf_password")

        if not password1 or not password2:
            raise ValidationError('La contraseña es obligatoria.')

        if password1 != password2:
            raise ValidationError('Las contraseñas no coinciden.')

        if len(password1) < 6 or not any(char.isupper() for char in password1) or not any(char.isdigit() for char in password1):
            raise ValidationError('La contraseña debe tener al menos 6 caracteres, incluir una letra mayúscula y un número.')
        
        if User.objects.filter(username=username).exclude(pk=self.instance.user.pk if self.instance and self.instance.pk else None).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        
        if User.objects.filter(email=email).exclude(pk=self.instance.user.pk if self.instance and self.instance.pk else None).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")
        
        if Administrador.objects.filter(numero_documento=numero_documento).exclude(pk=self.instance.pk if self.instance and self.instance.pk else None).exists():
            raise ValidationError("Este número de documento ya está registrado.")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if self.instance.pk:
            user = self.instance.user
            if username and user.username != username:
                user.username = username
            if email and user.email != email:
                user.email = email
            if password:
                user.set_password(password)
            user.save()
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
        
        administrador = super().save(commit=False)
        administrador.user = user
        if commit:
            administrador.save()
        return administrador

    class Meta:
        model = Administrador
        fields = ["username", "email", "nombre", "tipo_documento", "numero_documento", "telefono", "password", "conf_password"]
        widgets = {
            "nombre": TextInput(attrs={"placeholder": "Nombre del administrador"}),
            "tipo_documento": Select(attrs={"placeholder": "Tipo de documento"}),
            "numero_documento": NumberInput(attrs={"min": 8, "placeholder": "Número de documento"}),
            "telefono": NumberInput(attrs={"min": 1, "placeholder": "Teléfono"}),
            "password": PasswordInput(attrs={"min": 1, "placeholder": "Contraseña"}),
            "conf_password": PasswordInput(attrs={"min": 1, "placeholder": "Confirme su contraseña"})
        }

############################################################################

class OperadorForm(ModelForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Nombre de usuario"})
    )
    email = forms.EmailField(
        label="Email",
        max_length=150,
        widget=forms.EmailInput(attrs={"placeholder": "Correo electrónico"})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=PasswordInput(attrs={"placeholder": "Contraseña"}),
        required=False
    )
    conf_password = forms.CharField(
        label="Confirmar contraseña",
        widget=PasswordInput(attrs={"placeholder": "Confirmar contraseña"}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["autofocus"] = True
        
        if self.instance and self.instance.pk and hasattr(self.instance, 'user'):
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("conf_password")
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        numero_documento = cleaned_data.get('numero_documento')
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("conf_password")

        if not password1 or not password2:
            raise ValidationError('La contraseña es obligatoria.')

        if password1 != password2:
            raise ValidationError('Las contraseñas no coinciden.')

        if len(password1) < 6 or not any(char.isupper() for char in password1) or not any(char.isdigit() for char in password1):
            raise ValidationError('La contraseña debe tener al menos 6 caracteres, incluir una letra mayúscula y un número.')
        
        if User.objects.filter(username=username).exclude(pk=self.instance.user.pk if self.instance and self.instance.pk else None).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        
        if User.objects.filter(email=email).exclude(pk=self.instance.user.pk if self.instance and self.instance.pk else None).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")
        
        if Administrador.objects.filter(numero_documento=numero_documento).exclude(pk=self.instance.pk if self.instance and self.instance.pk else None).exists():
            raise ValidationError("Este número de documento ya está registrado.")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if self.instance.pk and hasattr(self.instance, 'user'):
            user = self.instance.user
            user.username = username
            user.email = email
            if password:
                user.set_password(password)
            user.save()
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password or None  
            )
            self.instance.user = user 

        operador = super().save(commit=False)
        operador.contrasena = password if password else operador.contrasena
        operador.conf_contrasena = cleaned_data.get('conf_password') if password else operador.conf_contrasena
        if commit:
            operador.save()
        return operador

    class Meta:
        model = Operador
        fields = ["username", "email", "nombre", "tipo_documento", "numero_documento", "telefono", "password", "conf_password"]
        widgets = {
            "nombre": TextInput(attrs={"placeholder": "Nombre del operador"}),
            "tipo_documento": Select(attrs={"placeholder": "Tipo de documento"}),
            "numero_documento": NumberInput(attrs={"min": 8, "placeholder": "Número de documento"}),
            "telefono": NumberInput(attrs={"min": 1, "placeholder": "Teléfono"}),
            "password": PasswordInput(attrs={"min": 1, "placeholder": "Contraseña"}),
            "conf_password": PasswordInput(attrs={"min": 1, "placeholder": "Confirme su contraseña"})
        }

#############################################################################

class MovimientoForm(ModelForm):
    class Meta:
        model = Movimiento
        fields = "__all__"
        exclude = ['fecha_mov']
        widgets = {
            "motivo": TextInput(
                attrs={
                    'id': 'motivo',
                    'placeholder': 'Motivo',
                    'class': 'form-control',
                    'name': "motivo",
                }
            ),
            
        }