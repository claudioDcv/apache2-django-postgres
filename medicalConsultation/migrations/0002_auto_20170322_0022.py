# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 03:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicalConsultation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalConsultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Titulo')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicalConsultation.Patient', verbose_name='paciente')),
            ],
            options={
                'verbose_name': 'consulta medica',
                'verbose_name_plural': 'consultas medicas',
            },
        ),
        migrations.CreateModel(
            name='Veterinarian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=40)),
                ('last_name', models.CharField(blank=True, max_length=40)),
                ('tagline', models.CharField(blank=True, max_length=140)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='dogcolor',
            options={'verbose_name': 'color', 'verbose_name_plural': 'colores'},
        ),
        migrations.AlterField(
            model_name='dogbreed',
            name='code',
            field=models.CharField(max_length=200, unique=True, verbose_name='Código'),
        ),
        migrations.AlterField(
            model_name='dogbreed',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='dogcolor',
            name='code',
            field=models.CharField(max_length=100, unique=True, verbose_name='Código'),
        ),
        migrations.AlterField(
            model_name='dogcolor',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='medicalconsultation',
            name='veterinarian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicalConsultation.Veterinarian', verbose_name='veterinario'),
        ),
    ]
