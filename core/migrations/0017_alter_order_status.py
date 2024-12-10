# Generated by Django 5.1.3 on 2024-12-09 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_commandelivraison'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'En attente'), ('En attente', 'Payée'), ('shipped', 'Expédiée'), ('servit', 'Servit')], default='pending', max_length=50),
        ),
    ]