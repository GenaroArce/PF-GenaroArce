from django.db import models
from django.contrib.auth.models import User

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    email = models.EmailField()
    grado = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    profesor = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.nombre

class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.estudiante.apellido} - {self.estudiante.grado} - {self.nota} - {self.materia.nombre} - {self.materia.profesor}"
    
class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatars")   
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.imagen}"