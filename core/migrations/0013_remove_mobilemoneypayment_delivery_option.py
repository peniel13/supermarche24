# Generated by Django 5.1.3 on 2024-12-06 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_mobilemoneypayment_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobilemoneypayment',
            name='delivery_option',
        ),
    ]
