# Generated by Django 5.1.3 on 2024-12-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_mobilemoneypayment_delivery_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobilemoneypayment',
            name='activated',
        ),
        migrations.RemoveField(
            model_name='mobilemoneypayment',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='mobilemoneypayment',
            name='verified_at',
        ),
        migrations.AddField(
            model_name='mobilemoneypayment',
            name='delivery_option',
            field=models.CharField(choices=[('home', 'A domicile'), ('pickup', 'Récupérer soi-même')], default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mobilemoneypayment',
            name='phone_number',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mobilemoneypayment',
            name='status',
            field=models.CharField(choices=[('pending', 'En attente'), ('validated', 'Validé'), ('rejected', 'Rejeté')], default='pending', max_length=10),
        ),
    ]
