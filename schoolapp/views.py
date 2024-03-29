from django.shortcuts import render, redirect
from .models import *
from .forms import EstudianteForm, MateriaForm, CrearNotaForm, BuscarEstudiantesForm, CustomUserCreationForm, CustomAuthenticationForm, EditarPerfilForm, CambiarContraseñaForm, AvatarForm
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'schoolapp/home.html')

@login_required
def aboutme(request):
    return render(request, 'schoolapp/aboutme.html')

@login_required
def agregar_nota(request):
    if request.method == 'POST':
        form = CrearNotaForm(request.POST)
        if form.is_valid():
            estudiante = form.cleaned_data['estudiante']
            materia = form.cleaned_data['materia']
            nota = form.cleaned_data['nota']
            Nota.objects.create(estudiante=estudiante, materia=materia, nota=nota)
            messages.success(request, 'La nota se ha agregado con éxito.')
            return redirect('home') 
    else:
        form = CrearNotaForm()
    return render(request, 'schoolapp/agregar_notas.html', {'form': form})

@login_required
def agregar_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save(commit=False)
            grado = int(estudiante.grado)
            if grado == 1:
                estudiante.grado = '1ro'
            elif grado == 2:
                estudiante.grado = '2do'
            elif grado == 3:
                estudiante.grado = '3ro'
            elif grado == 4:
                estudiante.grado = '4to'
            elif grado == 5:
                estudiante.grado = '5to'
            elif grado == 6:
                estudiante.grado = '6to'
            else:
                estudiante.grado = 'Otro'
            
            estudiante.save()
            messages.success(request, 'El estudiante se ha agregado con éxito.')
            
            return redirect('home')
    else:
        form = EstudianteForm()
    return render(request, 'schoolapp/agregar_estudiante.html', {'form': form})

@login_required
def lista_estudiantes(request):
    if request.method == 'POST':
        form = BuscarEstudiantesForm(request.POST)
        if form.is_valid():
            grado = form.cleaned_data['grado']
            materia = form.cleaned_data['materia']
            estudiantes = Estudiante.objects.filter(grado=grado)
            for estudiante in estudiantes:
                estudiante.notas = estudiante.nota_set.filter(materia=materia)
            estudiantes_con_notas = [estudiante for estudiante in estudiantes if estudiante.notas.exists()]
            return render(request, 'schoolapp/lista_estudiantes.html', {'estudiantes': estudiantes_con_notas, 'materia': materia})
    else:
        form = BuscarEstudiantesForm()
    return render(request, 'schoolapp/buscar_estudiantes.html', {'form': form})

@login_required
def agregar_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La materia se ha agregado con éxito.')
            return redirect('home') 
    else:
        form = MateriaForm()
    return render(request, 'schoolapp/agregar_materia.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Registro exitoso. Por favor, inicia sesión.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo '{field}': {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'schoolapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                try:
                    avatar = Avatar.objects.get(user=request.user.id).imagen.url
                except:
                    avatar = "/media/avatars/default.png"
                finally:
                    request.session["avatar"] = avatar
                return redirect('home')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'schoolapp/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        password_form = CambiarContraseñaForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('home')
        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Contraseña cambiada correctamente.')
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            for error in password_form.errors.values():
                messages.error(request, error)
    else:
        form = EditarPerfilForm(instance=request.user)
        password_form = CambiarContraseñaForm(request.user)
    return render(request, 'schoolapp/editar_perfil.html', {'form': form, 'password_form': password_form})

@login_required
def agregar_avatar(request):
    if request.method == "POST":
        miForm = AvatarForm(request.POST, request.FILES)

        if miForm.is_valid():
            usuario = User.objects.get(username=request.user)
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            avatar = Avatar(user=usuario,
                            imagen=miForm.cleaned_data["imagen"])
            avatar.save()
            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session["avatar"] = imagen
            
            return redirect('home')
    else:
        miForm = AvatarForm()

    return render(request, "schoolapp/agregar_avatar.html", {"form": miForm} )      