# Generated by Django 4.2.2 on 2024-03-28 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MateriaCrear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_materia', models.CharField(max_length=100)),
                ('nombre_profesor', models.CharField(max_length=100)),
            ],
        ),
    ]
