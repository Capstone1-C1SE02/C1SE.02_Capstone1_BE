# Generated by Django 5.0.3 on 2024-04-12 15:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0007_remove_degree_book_studentid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Degree_Book',
            fields=[
                ('DegreeBookID', models.AutoField(primary_key=True, serialize=False)),
                ('NumberOfGraduationDecision', models.CharField(max_length=50)),
                ('GraduationDecisionDate', models.DateField()),
                ('NumberInTheDegreeBook', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Degree_Infomation',
            fields=[
                ('DegreeID', models.AutoField(primary_key=True, serialize=False)),
                ('Classification', models.CharField(max_length=50)),
                ('YearOfGraduation', models.CharField(max_length=50)),
                ('SerialNumber', models.CharField(max_length=50)),
                ('DegreeBookID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adminapp.degree_book')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('StudentID', models.AutoField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(max_length=50)),
                ('LastName', models.CharField(max_length=50)),
                ('Gender', models.BooleanField()),
                ('DateOfBirth', models.DateField()),
                ('Address', models.CharField(max_length=50)),
                ('Nation', models.CharField(max_length=50)),
                ('Nationality', models.CharField(max_length=50)),
                ('PhoneNumber', models.CharField(max_length=50, null=True)),
                ('Email', models.EmailField(max_length=50, null=True)),
                ('MSSV', models.CharField(max_length=50)),
                ('YearOfAdmission', models.CharField(max_length=50)),
                ('YBAP_ID', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminapp.year_based_academic_program')),
            ],
        ),
        migrations.AddField(
            model_name='degree_book',
            name='StudentID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.student'),
        ),
    ]