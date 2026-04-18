from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# Creamos nuestro propio formulario heredando del original de Django
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',) # Los campos de contraseña se añaden solos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # nombre de usuario
        self.fields['username'].widget.attrs.update({
            'class': 'register-name-user',
            'placeholder': 'Nombre de Usuario'
        })
        
        # primera contraseña
        self.fields['password1'].widget.attrs.update({
            'id': 'id-register-password1',
            'class': 'register-password-user',
            'placeholder': 'Contraseña'
        })
        
        # confirmación de la contraseña
        self.fields['password2'].widget.attrs.update({
            'id': 'id-register-password1',
            'class': 'register-password-user',
            'placeholder': 'Repite Contraseña'
        })