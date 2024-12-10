# Generated by Django 5.1.3 on 2024-12-05 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_order_mobilemoneytransaction_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='store',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='MobileMoneyTransaction',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
