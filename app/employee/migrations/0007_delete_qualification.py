# Generated by Django 4.2.16 on 2024-10-28 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_remove_qualification_employee'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Qualification',
        ),
    ]
