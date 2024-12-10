# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import Order
# from decimal import Decimal

# @receiver(pre_save, sender=Order)
# def calculate_order_total(sender, instance, **kwargs):
#     if instance.total_amount == Decimal('0.00'):
#         instance.total_amount = sum(item.get_total_price() for item in instance.items.all())
