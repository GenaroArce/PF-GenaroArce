from django import forms
from .models import Estudiante, Materia, Nota
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

class EstudianteForm(forms.ModelForm):
    email = forms.EmailField(label='Correo Electrónico')

    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'edad', 'email', 'grado']

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nombre', 'profesor']

    def clean_nombre(self):
        nombre_materia = self.cleaned_data.get('nombre')
        return nombre_materia

    def clean_profesor(self):
        nombre_profesor = self.cleaned_data.get('profesor')
        return nombre_profesor

class CrearNotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['estudiante', 'materia', 'nota']

class BuscarEstudiantesForm(forms.Form):
    grado = forms.ChoiceField(choices=[('1ro', '1ro'), ('2do', '2do'), ('3ro', '3ro'), ('4to', '4to'), ('5to', '5to'), ('6to', '6to')])
    materia = forms.ModelChoiceField(queryset=Materia.objects.all())


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class EditarPerfilForm(UserChangeForm):
    password = None  

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Este email ya está en uso.')
        return email
    
class CambiarContraseñaForm(PasswordChangeForm):
    class Meta:
        model = User

class AvatarForm(forms.Form):
    imagen = forms.ImageField(required=True)