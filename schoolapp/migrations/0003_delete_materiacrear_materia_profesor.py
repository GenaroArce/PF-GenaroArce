# Generated by Django 4.2.2 on 2024-03-28 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0002_materiacrear'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MateriaCrear',
        ),
        migrations.AddField(
            model_name='materia',
            name='profesor',
            field=models.CharField(default='', max_length=100),
        ),
    ]
