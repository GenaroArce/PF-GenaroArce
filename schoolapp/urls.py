from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('sobre-mi/', aboutme, name='aboutme'),

    #____Funciones de Usuario
    path('agregar-nota/', agregar_nota, name='agregar_nota'),
    path('agregar-estudiante/', agregar_estudiante, name='agregar_estudiante'),
    path('agregar-materia/', agregar_materia, name='agregar_materia'),
    path('buscar-estudiantes/', lista_estudiantes, name='buscar_estudiantes'),

    #_____AUTHME - Registro, Login y Logout
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    #____Editar perfil
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    path('agregar-avatar/', agregar_avatar, name='agregar_avatar'),
]