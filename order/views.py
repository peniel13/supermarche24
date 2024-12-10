# import json
# import stripe
# from django.conf import settings
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from core.models import Cart, CartItem
# from .models import Order, OrderItem
# from django.contrib.auth.decorators import login_required

# @login_required
# def start_order(request):
#     # Récupérer le panier de l'utilisateur
#     cart = get_or_create_cart(request.user)
    
#     # Vérifier que le panier contient des articles
#     if cart.get_item_count() == 0:
#         return JsonResponse({'error': 'Le panier est vide'}, status=400)
    
#     data = json.loads(request.body)
    
#     total_price = 0
#     items = []

#     # Construire la liste des éléments pour Stripe
#     for item in cart.items.all():
#         product = item.product
#         total_price += product.price * item.quantity
#         items.append({
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': product.name,
#                 },
#                 'unit_amount': product.price * 100,  # Conversion en centimes
#             },
#             'quantity': item.quantity
#         })
    
#     # Configuration de Stripe
#     stripe.api_key = settings.STRIPE_API_SECRET_KEY

#     # Créer une session de paiement Stripe
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=items,
#         mode='payment',
#         success_url=request.build_absolute_uri('/cart/success/'),
#         cancel_url=request.build_absolute_uri('/cart/')
#     )

#     # Créer la commande
#     order = Order.objects.create(
#         user=request.user,
#         first_name=data['first_name'],
#         last_name=data['last_name'],
#         email=data['email'],
#         phone=data['phone'],
#         address=data['address'],
#         zipcode=data['zipcode'],
#         place=data['place'],
#         payment_intent=session.payment_intent,
#         paid=False,  # La commande n'est pas encore payée
#         paid_amount=total_price  # Total en centimes
#     )

#     # Créer les éléments de la commande
#     for item in cart.items.all():
#         OrderItem.objects.create(
#             order=order,
#             product=item.product,
#             price=item.product.price * item.quantity,
#             quantity=item.quantity
#         )

#     # Vider le panier après la création de la commande
#     cart.is_active = False  # Désactiver le panier une fois la commande passée
#     cart.save()

#     # Retourner la session Stripe pour rediriger l'utilisateur
#     return JsonResponse({'sessionId': session.id})
