# Generated by Django 4.2.16 on 2024-10-28 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_alter_employee_account_no_alter_employee_bank_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qualification',
            name='employee',
        ),
    ]
