# Generated by Django 5.0.3 on 2024-03-27 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_academic_year_degree_book_major_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degree_infomation',
            name='DegreeBookID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adminapp.degree_book'),
        ),
    ]
