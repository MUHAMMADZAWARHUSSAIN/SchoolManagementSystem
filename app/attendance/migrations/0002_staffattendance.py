# Generated by Django 5.1.1 on 2024-10-18 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
        ('employee', '0002_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('is_present', models.BooleanField(default=False)),
                ('is_late', models.BooleanField(default=False)),
                ('is_excused', models.BooleanField(default=False)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
        ),
    ]