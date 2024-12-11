from django.shortcuts import render, redirect
from .models import Store, Category, Product,Testimonial,CommandeLivraison
from .forms import StoreForm, CategoryForm, ProductForm,RegisterForm, UpdateProfileForm,TestimonialForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView  # DetailView pour afficher un objet, CreateView pour créer un nouvel objet
from django.urls import reverse


def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("signup")
        
    context = {"form":form}
    return render(request, "core/signup.html", context)

def signin (request):
    if request.method == 'POST':
        email = request.POST["email"]
        password= request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    context= {}
    return render(request, "core/login.html", context)

def signout(request):
    logout(request)
    return redirect("index")

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url="signin")
def profile(request):
    user = request.user
    stores = Store.objects.filter(owner=user)

    # Récupérer toutes les commandes de l'utilisateur
    orders_list = Order.objects.filter(user=request.user, activated=True).order_by('-created_at')
    
    # Récupérer toutes les commandes de livraison de l'utilisateur
    commandes_list = CommandeLivraison.objects.filter(user=user).order_by('-date_commande')
    paginator = Paginator(commandes_list, 4)  # 4 commandes par page
    page_number = request.GET.get('page')
    
    try:
        commandes = paginator.page(page_number)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, afficher la première page
        commandes = paginator.page(1)
    except EmptyPage:
        # Si la page est vide, afficher la dernière page
        commandes = paginator.page(paginator.num_pages)
    # Pagination - Afficher 4 commandes par page
    paginator = Paginator(orders_list, 4)  # 4 commandes par page
    page_number = request.GET.get('page')
    
    try:
        orders = paginator.page(page_number)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, afficher la première page
        orders = paginator.page(1)
    except EmptyPage:
        # Si la page est vide, afficher la dernière page
        orders = paginator.page(paginator.num_pages)

    context = {
        "user": user,
        "stores": stores,
        "orders": orders,  # Orders paginées
        "commandes": commandes,
    }
    
    return render(request, "core/profile.html", context)




@login_required(login_url="signin")
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = UpdateProfileForm(instance=user)
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully")
                return redirect("profile")
                
    context = {"form": form}
    return render(request, "core/update_profile.html", context)
# # Créer une boutique

# def create_store(request):
#     if request.method == 'POST':
#         form = StoreForm(request.POST)
#         if form.is_valid():
#             store = form.save(commit=False)
#             store.owner = request.user
#             store.save()
#             return redirect('shop:store_detail', store_id=store.id)
#     else:
#         form = StoreForm()
#     return render(request, 'core/create_store.html', {'form': form})
@login_required
def create_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, initial={'user': request.user})
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user  # Associer l'utilisateur à ce store
            store.save()

            messages.success(request, "Votre store a été créé avec succès !")
            return redirect('profile')  # Redirection après succès
    else:
        form = StoreForm(initial={'user': request.user})

    return render(request, 'core/create_store.html', {'form': form})

@login_required
def edit_store(request, slug):
    store = get_object_or_404(Store, slug=slug, owner=request.user)  # Lookup by slug instead of ID
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, "Le store a été mis à jour avec succès !")
            return redirect('profile')  # Or wherever you want to redirect after editing
    else:
        form = StoreForm(instance=store)

    return render(request, 'core/edit_store.html', {'form': form, 'store': store})

# delete store
@login_required
def delete_store(request, slug):
    store = get_object_or_404(Store, slug=slug, owner=request.user)  # Lookup by slug instead of ID
    if request.method == 'POST':
        store.delete()
        messages.success(request, "Le store a été supprimé avec succès !")
        return redirect('profile')  # Or wherever you want to redirect after deletion
    return render(request, 'core/delete_store.html', {'store': store})

# Créer une catégorie
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Store
from .forms import CategoryForm
from django.http import HttpResponseForbidden


# @login_required
# def create_category(request, slug):
#     # Get the store using the slug and ensure the logged-in user is the owner
#     store = get_object_or_404(Store, slug=slug, owner=request.user)
    
#     # Handle category creation
#     if request.method == 'POST' and 'create_category' in request.POST:
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.store = store
#             category.save()
#             messages.success(request, "Catégorie créée avec succès!")
#             return redirect('store_detail', slug=store.slug)  # Refresh the page to show the new category
#     else:
#         form = CategoryForm()

#     # Get all categories for this store
#     categories = Category.objects.filter(store=store)

#     return render(request, 'core/create_category.html', {'form': form, 'store': store, 'categories': categories})
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Category, Store
from .forms import CategoryForm

@login_required
def create_category(request, store_id):
    # Récupérer le store via son id et s'assurer que l'utilisateur est le propriétaire
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    # Créer une nouvelle catégorie
    if request.method == 'POST' and 'create_category' in request.POST:
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.store = store
            category.save()
            messages.success(request, "Catégorie créée avec succès!")
            return redirect('create_category', store_id=store.id)  # Redirection pour éviter une soumission multiple
    else:
        form = CategoryForm()

    # Gérer la suppression d'une catégorie
    if request.method == 'POST' and 'delete_category' in request.POST:
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id, store=store)
        category.delete()
        messages.success(request, "Catégorie supprimée avec succès!")
        return redirect('create_category', store_id=store.id)

    # Gérer la modification d'une catégorie
    if request.method == 'POST' and 'edit_category' in request.POST:
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id, store=store)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie mise à jour avec succès!")
            return redirect('create_category', store_id=store.id)

    # Récupérer toutes les catégories existantes pour le store
    categories = Category.objects.filter(store=store)

    return render(request, 'core/create_category.html', {
        'form': form,
        'store': store,
        'categories': categories
    })

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Category, Store

@login_required
def list_categories(request, store_id):
    # Récupérer le store via son ID et s'assurer que l'utilisateur est le propriétaire
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    # Supprimer une catégorie
    if request.method == 'POST' and 'delete_category' in request.POST:
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id, store=store)
        category.delete()
        messages.success(request, "Catégorie supprimée avec succès!")
        return redirect('list_categories', store_id=store.id)

    # Récupérer toutes les catégories pour le store
    categories = Category.objects.filter(store=store)

    return render(request, 'core/list_categories.html', {
        'store': store,
        'categories': categories,
    })


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Category
from .forms import CategoryForm

@login_required
def edit_category(request, slug):
    # Récupérer le store auquel les catégories appartiennent
    store = get_object_or_404(Store, slug=slug, owner=request.user)
    
    # Récupérer toutes les catégories du store
    categories = Category.objects.filter(store=store)

    if request.method == 'POST':
        # Si un formulaire de modification ou de suppression est soumis
        if 'edit_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id, store=store)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "Catégorie modifiée avec succès!")
                return redirect('edit_category', slug=store.slug)
        
        elif 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id, store=store)
            category.delete()
            messages.success(request, "Catégorie supprimée avec succès!")
            return redirect('edit_category', slug=store.slug)

    return render(request, 'core/edit_category.html', {'store': store, 'categories': categories})

# Créer un produit
@login_required
def create_product(request, store_id):
    store = Store.objects.get(id=store_id, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('store_detail', store_id=store.id)
    else:
        form = ProductForm()
    return render(request, 'core/create_product.html', {'form': form, 'store': store})

# Détails d'une boutique
def store_detail(request, store_id):
    store = Store.objects.get(id=store_id)
    return render(request, 'core/store_detail.html', {'store': store})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Fonction utilitaire pour obtenir ou créer un panier
def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user, is_ordered=False)
    return cart

# Ajouter un produit au panier
from django.http import JsonResponse

# @login_required
# def add_to_cart_ajax(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart = get_or_create_cart(request.user)

#     # Vérifier si l'article est déjà dans le panier
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not created:
#         cart_item.quantity += 1
#     else:
#         cart_item.quantity = 1
#     cart_item.save()

#     # Calculer le nombre total d'articles et le total du panier
#     total_items = cart.get_item_count()
#     total_price = cart.get_total()

#     # Retourner ces informations sous forme de réponse JSON
#     return JsonResponse({'total_items': total_items, 'total_price': total_price})
from .models import Cart, CartItem

# @login_required
# def add_to_cart_ajax(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart = get_or_create_cart(request.user)

#     # Vérifier si l'article est déjà dans le panier
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not created:
#         cart_item.quantity += 1
#     else:
#         cart_item.quantity = 1
#     cart_item.save()

#     # Calculer le nombre total d'articles et le total du panier
#     total_items = cart.get_item_count()
#     total_price = cart.get_total()

#     # Retourner ces informations sous forme de réponse JSON
#     return JsonResponse({'total_items': total_items, 'total_price': total_price})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# @login_required
# def add_to_cart_ajax(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart = get_or_create_cart(request.user)

#     # Vérifier si l'article est déjà dans le panier
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not created:
#         cart_item.quantity += 1
#     else:
#         cart_item.quantity = 1
#     cart_item.save()

#     # Calculer le nombre total d'articles et le total du panier
#     total_items = cart.get_item_count()
#     total_price = cart.get_total()

#     # Rediriger vers la page de confirmation
#     return redirect('add_to_cart_success')  # Redirige vers la page de succès
@login_required(login_url="signin")
def add_to_cart_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request.user)

    # Vérifier si l'article est déjà dans le panier
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()

    # Calculer le nombre total d'articles dans le panier
    total_items = cart.get_item_count()

    # Retourner la redirection mais aussi mettre à jour dynamiquement la page de confirmation
    return redirect('add_to_cart_success')


from django.http import JsonResponse
from .models import Cart

@login_required
def get_cart_items_count(request):
    cart = get_or_create_cart(request.user)
    total_items = cart.get_item_count()
    return JsonResponse({
        'total_items': total_items,
    })

def context_processors(request):
    if request.user.is_authenticated:
        cart = get_or_create_cart(request.user)
    else:
        cart = None
    return {'cart': cart}

def get_or_create_cart(user):
    """
    Cette fonction vérifie si l'utilisateur a déjà un panier actif.
    Si oui, il le retourne. Sinon, il crée un nouveau panier.
    """
    cart, created = Cart.objects.get_or_create(user=user, is_active=True)
    return cart


from django.shortcuts import render

@login_required(login_url="signin")
def add_to_cart_success(request):
    # Obtenez le panier de l'utilisateur
    cart = get_or_create_cart(request.user)
    total_items = cart.get_item_count()
    total_price = cart.get_total()

    # Utilisez le related_name 'items' pour accéder aux articles du panier
    last_added_product = cart.items.last().product if cart.items.exists() else None

    return render(request, 'core/add_to_cart_success.html', {
        'product': last_added_product,
        'total_items': total_items,
        'total_price': total_price,
    })


# Voir le contenu du panier
from .models import Cart

@login_required(login_url="signin")
def cart_detail(request):
    # Récupère ou crée le panier de l'utilisateur connecté
    cart = get_or_create_cart(request.user)
    
    context = {
        'cart': cart
    }
    
    return render(request, 'core/cart_detail.html', context)
# @login_required
# def cart_detail(request):
#     # Récupère ou crée le panier de l'utilisateur connecté
#     cart = get_or_create_cart(request.user)

#     # Crée la commande à partir du panier si elle n'existe pas
#     if not cart.is_ordered:
#         order = Order.objects.create(
#             user=request.user,
#             store=cart.items.first().product.store,  # Associe la commande au premier magasin dans le panier
#         )
#         for item in cart.items.all():
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 price_at_time_of_order=item.product.price
#             )
#         order.calculate_total()
#         cart.is_ordered = True
#         cart.save()
#     else:
#         # Si le panier est déjà commandé, récupère la commande existante
#         order = Order.objects.filter(user=request.user, status='pending').first()

#     context = {
#         'cart': cart,
#         'order': order  # Assure-toi de passer `order` dans le contexte
#     }

#     return render(request, 'core/cart_detail.html', context)


# Modifier la quantité d'un produit dans le panier
@login_required
def update_cart(request, cart_item_id, quantity):
    # Récupérer l'élément du panier correspondant
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    # Si la quantité vient du formulaire POST, l'utiliser à la place de celle dans l'URL
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', cart_item.quantity))  # Si pas de quantity dans le POST, conserver l'ancienne

    # Si la quantité est inférieure ou égale à zéro, supprimer l'élément du panier
    if quantity <= 0:
        cart_item.delete()
    else:
        # Sinon, mettre à jour la quantité
        cart_item.quantity = quantity
        cart_item.save()
    
    # Rediriger vers la vue du panier
    return redirect('cart_detail')




# Supprimer un produit du panier
@login_required
def remove_from_cart(request, cart_item_id):
    # Récupérer l'élément du panier correspondant
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    
    # Supprimer l'élément du panier
    cart_item.delete()
    
    # Rediriger vers la vue du panier
    return redirect('cart_detail')


from django.contrib.auth.mixins import LoginRequiredMixin

class TestimonialCreateView(LoginRequiredMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'testimonial_form.html'  # Créez ce template pour le formulaire
    context_object_name = 'form'

    def form_valid(self, form):
        form.instance.user = self.request.user  # L'utilisateur actuel est assigné au témoignage
        form.instance.store = Store.objects.get(id=self.kwargs['pk'])  # Associe le témoignage au magasin
        return super().form_valid(form)

    def get_success_url(self):
        store_id = self.kwargs['pk']
        return reverse('store_detail', kwargs={'pk': store_id}) 
         
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Cart

# @login_required
# def checkout(request):
#     # Récupérer ou créer le panier de l'utilisateur
#     cart = get_or_create_cart(request.user)
    
#     # Calculer le total du panier et le diviser par 100 pour obtenir la valeur en dollars
#     total_price_in_cents = cart.get_total()
#     total_price_in_dollars = total_price_in_cents / 100  # Conversion en dollars

#     # Passer les valeurs au template
#     pub_key = settings.STRIPE_API_KEY_PUBLISHABLE

#     return render(request, 'core/checkout.html', {
#         'pub_key': pub_key,
#         'cart': cart,
#         'total_price_in_dollars': total_price_in_dollars
#     })


# def success(request):
#     return render(request, 'core/success.html',)

from django.shortcuts import render, redirect
from .models import Cart, CartItem, Order, OrderItem, Product
from django.contrib.auth.decorators import login_required
from django.http import Http404

@login_required
def payment_success(request):
    # Récupérer le panier de l'utilisateur
    cart = get_or_create_cart(request.user)
   
    if cart.get_item_count() == 0:
        return redirect('cart_detail')
   
    # Créer une commande
    order = Order.objects.create(
        user=request.user,
        store=cart.items.first().product.store,  # Utilise le store du premier produit du panier
        status='paid',
    )
   
    # Ajouter les articles de la commande
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price_at_time_of_order=cart_item.product.price
        )

    # Mettre à jour le total de la commande
    order.calculate_total()

    # Vider le panier de l'utilisateur après la commande
    cart.items.all().delete()

    # Retourner à la page de confirmation
    return render(request, 'core/payment_success.html', {'order': order})

# payement mobile money

@login_required
def mobile_money_payment_success(request):
    # Récupérer le paiement Mobile Money validé
    payment = MobileMoneyPayment.objects.filter(user=request.user, activated=True).last()
    
    if not payment:
        return redirect('mobile_money_checkout')  # Si aucun paiement validé, rediriger

    # Créer une commande pour Mobile Money
    cart = get_or_create_cart(request.user)
    order = Order.objects.create(
        user=request.user,
        store=cart.items.first().product.store,
        status='paid',
    )

    # Ajouter les articles de la commande
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price_at_time_of_order=cart_item.product.price
        )

    order.calculate_total()  # Mettre à jour le total de la commande

    # Vider le panier de l'utilisateur après la commande
    cart.items.all().delete()

    return render(request, 'core/mobile_money_payment_success.html', {'order': order})
# views.py
@login_required
def mobile_money_waiting(request, payment_id):
    payment = get_object_or_404(MobileMoneyPayment, id=payment_id, user=request.user)

    if payment.status == 'validated':  # Si le paiement est validé, on redirige vers la page de succès
        return redirect('mobile_money_payment_success')

    return render(request, 'core/mobile_money_waiting.html', {'payment': payment})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MobileMoneyPaymentForm
from .models import MobileMoneyPayment, Order, OrderItem


@login_required
def mobile_money_checkout(request):
    # Vérifier si le panier est vide
    cart = get_or_create_cart(request.user)
    if cart.get_item_count() == 0:
        return redirect('core/cart_detail')  # Si le panier est vide, on redirige

    # Calculer le total des articles et le montant total
    total_items = cart.get_item_count()
    total_amount = sum(item.product.price * item.quantity for item in cart.items.all())

    if request.method == 'POST':
        form = MobileMoneyPaymentForm(request.POST)
        if form.is_valid():
            # Sauvegarder le paiement Mobile Money
            payment = form.save(commit=False)
            payment.user = request.user
            payment.status = 'pending'  # Statut initial en attente
            payment.save()

            # Créer l'ordre mais avec 'activated' = False (désactivé pour Mobile Money)
            order = Order.objects.create(
                user=request.user,
                store=cart.items.first().product.store,  # Le store est celui du premier produit du panier
                status='pending',
                activated=False  # Désactivé par défaut pour Mobile Money
            )

            # Ajouter les articles de la commande
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_at_time_of_order=cart_item.product.price
                )

            # Calculer le total de la commande
            order.calculate_total()

            # Vider le panier de l'utilisateur après la commande
            cart.items.all().delete()  # Suppression des articles dans le panier

            # Message de succès et redirection vers la page d'attente
            messages.success(request, 'Votre paiement Mobile Money a été soumis avec succès. Veuillez attendre la validation de l\'admin.')
            return redirect('mobile_money_waiting', payment_id=payment.id)
    else:
        form = MobileMoneyPaymentForm()

    return render(request, 'core/mobile_money_checkout.html', {
        'form': form,
        'total_items': total_items,
        'total_amount': total_amount
    })



import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart
from django.contrib.auth.decorators import login_required

# Configurer Stripe avec la clé secrète
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@login_required
def checkout(request):
    # Récupérer le panier de l'utilisateur
    cart = get_or_create_cart(request.user)
    if cart.get_item_count() == 0:
        return redirect('core/cart_detail')  # Si le panier est vide, on redirige

    # Créer une session de checkout de Stripe
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'eur',  # Monnaie de la transaction
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100),  # Montant en cents
                },
                'quantity': item.quantity,
            }
            for item in cart.items.all()
        ],
        mode='payment',
        success_url=request.build_absolute_uri('https://supermarche24.onrender.com/user/payment_success/'),
        cancel_url=request.build_absolute_uri('https://supermarche24.onrender.com/user/payment_cancel/'),
    )

    # Rediriger l'utilisateur vers la page de paiement Stripe
    return redirect(checkout_session.url, code=303)

# Page de succès après un paiement réussi


# Page de cancellation en cas d'annulation de paiement
def payment_cancel(request):
    return render(request, 'core/payment_cancel.html')
# @login_required
# def checkout(request):
#     cart = get_or_create_cart(request.user)
#     if cart.get_item_count() == 0:
#         return redirect('shop:cart_detail')  # Rediriger si le panier est vide
   
#     # Ici, tu peux ajouter la logique de paiement (par exemple, intégration avec Stripe)
#     # Mais pour l'instant, nous simulons juste le processus de commande.

#     # Marquer le panier comme "commandé" pour éviter qu'il soit modifié après
#     cart.is_ordered = True
#     cart.save()
   
#     return render(request, 'shop/checkout.html', {'cart': cart})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Store, Category, Product
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Store, Product, Category

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Store, Product, Category

# def store_detail(request, slug):
#     # Récupère le store en fonction du slug
#     store = get_object_or_404(Store, slug=slug)
    
#     # Récupère les catégories associées au store
#     categories = Category.objects.filter(store=store)

#     # Récupère les produits associés au store
#     products = Product.objects.filter(store=store)

#     # Filtre par catégorie
#     category_filter = request.GET.get('categorie', '')  # Remarquez que 'categorie' est la clé
#     if category_filter:
#         # Filtrer les produits par l'ID de la catégorie sélectionnée
#         products = products.filter(category__id=category_filter)  # Filtrage correct par nom de catégorie

#     # Filtre par nom de produit
#     product_name = request.GET.get('nom', '')  # 'nom' est la clé utilisée dans le template
#     if product_name:
#         products = products.filter(name__icontains=product_name)  # Filtrage par nom de produit

#     # Filtre par prix
#     prix_min = request.GET.get('prix_min', '')  # 'prix_min' récupéré de la requête
#     prix_max = request.GET.get('prix_max', '')  # 'prix_max' récupéré de la requête
#     if prix_min:
#         try:
#             prix_min = float(prix_min)  # S'assurer que c'est un nombre valide
#             products = products.filter(price__gte=prix_min)
#         except ValueError:
#             pass  # Ignorer si le prix min n'est pas valide
#     if prix_max:
#         try:
#             prix_max = float(prix_max)  # S'assurer que c'est un nombre valide
#             products = products.filter(price__lte=prix_max)
#         except ValueError:
#             pass  # Ignorer si le prix max n'est pas valide

#     # Pagination
#     paginator = Paginator(products, 6)  # 6 produits par page
#     page = request.GET.get('page')

#     try:
#         products = paginator.page(page)
#     except PageNotAnInteger:
#         products = paginator.page(1)
#     except EmptyPage:
#         products = paginator.page(paginator.num_pages)

#     # Passer les données au template
#     context = {
#         'store': store,
#         'categories': categories,
#         'products': products,
#         'paginator': paginator,
#         'category_filter': category_filter,
#         'product_name': product_name,
#         'prix_min': prix_min,
#         'prix_max': prix_max,
#     }

#     return render(request, 'core/store_detail.html', context)

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Store, Category, Product, Testimonial
from django.db.models import Count, Sum
from .forms import TestimonialForm
from django.db.models.functions import TruncDate
from django.db.models import Avg

def store_detail(request, slug):
    # Récupère le store en fonction du slug
    store = get_object_or_404(Store, slug=slug)
    
    # Récupère les catégories associées au store
    categories = Category.objects.filter(store=store)

    # Récupère les produits associés au store
    products = Product.objects.filter(store=store).order_by('-created_at')
    for product in products:
        # Récupère tous les témoignages pour ce produit
        testimonials = Testimonialproduct.objects.filter(product=product)
        
        # Calcule la moyenne des notes si des témoignages existent
        if testimonials.exists():
            product.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
        else:
            product.average_rating = 0
    # Créez une plage de 1 à 10 pour les étoiles
    range_10 = range(1, 11)
    
    # Filtre par catégorie
    category_filter = request.GET.get('categorie', '')
    if category_filter:
        products = products.filter(category__id=category_filter)

    # Filtre par nom de produit
    product_name = request.GET.get('nom', '')
    if product_name:
        products = products.filter(name__icontains=product_name)

    # Filtre par prix
    prix_min = request.GET.get('prix_min', '')
    prix_max = request.GET.get('prix_max', '')
    if prix_min:
        try:
            prix_min = float(prix_min)
            products = products.filter(price__gte=prix_min)
        except ValueError:
            pass
    if prix_max:
        try:
            prix_max = float(prix_max)
            products = products.filter(price__lte=prix_max)
        except ValueError:
            pass

    # Pagination pour les produits
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Formulaire de témoignage
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.store = store
            testimonial.user = request.user
            testimonial.save()
            return redirect('store_detail', slug=slug)  # Redirige après ajout du témoignage
    else:
        form = TestimonialForm()

    # Pagination des témoignages
    testimonials = Testimonial.objects.filter(store=store)
    testimonial_paginator = Paginator(testimonials, 3)
    testimonial_page = request.GET.get('testimonial_page')
    try:
        testimonials = testimonial_paginator.page(testimonial_page)
    except PageNotAnInteger:
        testimonials = testimonial_paginator.page(1)
    except EmptyPage:
        testimonials = testimonial_paginator.page(testimonial_paginator.num_pages)
    
    # Initialiser les commandes
    orders_by_date = Order.objects.filter(store=store, activated=True) \
                                  .annotate(order_date=TruncDate('created_at'))  # Truncate 'created_at' to date only
    
    # Si la barre de recherche est utilisée pour filtrer par date
    order_date = request.GET.get('order_date', None)
    if order_date:
        try:
            # Convertir la date en format valide
            order_date = datetime.strptime(order_date, '%Y-%m-%d').date()
            orders_by_date = orders_by_date.filter(order_date=order_date)  # Filtrer par la date choisie
        except ValueError:
            messages.error(request, "La date fournie est invalide. Veuillez entrer une date correcte.")
            orders_by_date = []

    # Appliquer l'agrégation pour compter les commandes et calculer le montant total
    orders_by_date = orders_by_date.values('order_date')  # Regroupement par date
    orders_by_date = orders_by_date.annotate(
        total_orders=Count('id'),  # Nombre de commandes pour cette date
        total_amount_sum=Sum('total_amount')   # Somme des montants des commandes
    ).order_by('-order_date')  # Tri décroissant par date

    # Pagination des commandes par date
    order_paginator = Paginator(orders_by_date, 5)
    order_page = request.GET.get('order_page')
    try:
        orders_by_date_page = order_paginator.page(order_page)
    except PageNotAnInteger:
        orders_by_date_page = order_paginator.page(1)
    except EmptyPage:
        orders_by_date_page = order_paginator.page(order_paginator.num_pages)

    context = {
        'store': store,
        'categories': categories,
        'products': products,
        'paginator': paginator,
        'category_filter': category_filter,
        'product_name': product_name,
        'prix_min': prix_min,
        'prix_max': prix_max,
        'form': form,
        'testimonials': testimonials,
        'testimonial_paginator': testimonial_paginator,
        'range_10': range_10,
        'orders_by_date': orders_by_date_page,
        'order_date': order_date, 
        'order_paginator': order_paginator,
    }

    return render(request, 'core/store_detail.html', context)

# manage product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store, Product, Category
from .forms import ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@login_required
def manage_product_store(request, slug):
    store = get_object_or_404(Store, slug=slug, owner=request.user)
    products = Product.objects.filter(store=store).order_by('-created_at')

    categories = Category.objects.filter(store=store)

    category_filter = request.GET.get('categorie', '')
    if category_filter:
        products = products.filter(category__id=category_filter)

    product_name = request.GET.get('nom', '')
    if product_name:
        products = products.filter(name__icontains=product_name)

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'store': store,
        'products': products,
        'categories': categories,
        'paginator': paginator,
    }

    return render(request, 'core/manage_product_store.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Photo
from .forms import ProductForm, PhotoForm
@login_required

@login_required
def edit_product(request, product_id):
    # Récupère le produit à partir de son ID
    product = get_object_or_404(Product, id=product_id)

    # Vérifie que l'utilisateur est le propriétaire du magasin
    if product.store.owner != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce produit.")
        return redirect('manage_product_store', slug=product.store.slug)

    # Formulaire pour modifier les informations du produit
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit mis à jour avec succès.")
            
            # Traitement des images pour la galerie
            if 'image_galerie' in request.FILES:
                for image in request.FILES.getlist('image_galerie'):
                    photo = Photo(product=product, image=image)
                    photo.save()
                messages.success(request, "Images ajoutées à la galerie avec succès.")

            # Rediriger vers la page de gestion des produits du magasin
            return redirect('manage_product_store', slug=product.store.slug)
        else:
            messages.error(request, "Il y a des erreurs dans le formulaire.")
    else:
        form = ProductForm(instance=product)

    # Récupère les photos existantes associées au produit
    photos = product.photos.all()

    # Formulaire pour ajouter des photos à la galerie
    photo_form = PhotoForm()

    context = {
        'form': form,
        'photo_form': photo_form,
        'product': product,
        'photos': photos,
    }

    return render(request, 'core/edit_product.html', context)



from django.shortcuts import get_object_or_404, redirect
from .models import Photo

def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    product = photo.product
    if request.method == 'POST':
        photo.delete()
        return redirect('edit_product', product_id=product.id)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Vérifie que l'utilisateur est le propriétaire du produit ou du magasin
    if product.store.owner != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce produit.")
        return redirect('manage_product_store', slug=product.store.slug)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Produit supprimé avec succès.")
        return redirect('manage_product_store', slug=product.store.slug)
    else:
        messages.error(request, "La suppression a échoué. Essayez à nouveau.")
        return redirect('manage_product_store', slug=product.store.slug)


# @login_required
# def store_detail(request, slug):
#     # Récupère le store en fonction du slug
#     store = get_object_or_404(Store, slug=slug)
    
#     # Récupère les catégories associées au store
#     categories = Category.objects.filter(store=store)

#     # Récupère les produits associés au store
#     products = Product.objects.filter(store=store)
#     for product in products:
#         # Récupère tous les témoignages pour ce produit
#         testimonials = Testimonialproduct.objects.filter(product=product)
        
#         # Calcule la moyenne des notes si des témoignages existent
#         if testimonials.exists():
#             product.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
#         else:
#             product.average_rating = 0
#     # Créez une plage de 1 à 10 pour les étoiles
#     range_10 = range(1, 11)
    
#     # Filtre par catégorie
#     category_filter = request.GET.get('categorie', '')
#     if category_filter:
#         products = products.filter(category__id=category_filter)

#     # Filtre par nom de produit
#     product_name = request.GET.get('nom', '')
#     if product_name:
#         products = products.filter(name__icontains=product_name)

#     # Filtre par prix
#     prix_min = request.GET.get('prix_min', '')
#     prix_max = request.GET.get('prix_max', '')
#     if prix_min:
#         try:
#             prix_min = float(prix_min)
#             products = products.filter(price__gte=prix_min)
#         except ValueError:
#             pass
#     if prix_max:
#         try:
#             prix_max = float(prix_max)
#             products = products.filter(price__lte=prix_max)
#         except ValueError:
#             pass

#     # Pagination pour les produits
#     paginator = Paginator(products, 6)
#     page = request.GET.get('page')
#     try:
#         products = paginator.page(page)
#     except PageNotAnInteger:
#         products = paginator.page(1)
#     except EmptyPage:
#         products = paginator.page(paginator.num_pages)

#     # Formulaire de témoignage
#     if request.method == 'POST':
#         form = TestimonialForm(request.POST)
#         if form.is_valid():
#             testimonial = form.save(commit=False)
#             testimonial.store = store
#             testimonial.user = request.user
#             testimonial.save()
#             return redirect('store_detail', slug=slug)  # Redirige après ajout du témoignage
#     else:
#         form = TestimonialForm()

#     # Pagination des témoignages
#     testimonials = Testimonial.objects.filter(store=store)
#     testimonial_paginator = Paginator(testimonials, 3)
#     testimonial_page = request.GET.get('testimonial_page')
#     try:
#         testimonials = testimonial_paginator.page(testimonial_page)
#     except PageNotAnInteger:
#         testimonials = testimonial_paginator.page(1)
#     except EmptyPage:
#         testimonials = testimonial_paginator.page(testimonial_paginator.num_pages)
    
#     # initialiser
#     # Initialiser les commandes avec toutes les commandes pour ce magasin

#     # Récupérer la date spécifiée dans la barre de recherche (format yyyy-mm-dd)
    

#     # Si la barre de recherche est utilisée pour filtrer par date
#     orders_by_date = Order.objects.filter(store=store) \
#                                   .annotate(order_date=TruncDate('created_at')) \
#                                   .values('order_date') \
#                                   .distinct()

#     # Si la barre de recherche est utilisée pour filtrer par date
#     order_date = request.GET.get('order_date', None)
#     if order_date:
#         # Convertir la date en format valide
#         try:
#             order_date = datetime.strptime(order_date, '%Y-%m-%d').date()
#             orders_by_date = orders_by_date.filter(order_date=order_date)
#         except ValueError:
#             # Gérer le cas où la date est invalide
#             messages.error(request, "La date fournie est invalide. Veuillez entrer une date correcte.")
#             orders_by_date = []

#     # order par date
    
#     # Grouper les commandes par date (sans l'heure)
#     orders = Order.objects.filter(store=store)

#     # Regroupe par date en utilisant TruncDate et effectue les agrégations
#     orders_by_date = orders.annotate(
#         order_date=TruncDate('created_at')  # Truncate the timestamp to date
#     ).values('order_date')  # Extract the date for grouping

#     # Applique l'agrégation pour compter le nombre de commandes et la somme du montant
#     orders_by_date = orders_by_date.annotate(
#         total_orders=Count('id'),
#         total_amount=Sum('total_amount')
#     ).order_by('-order_date')  # Tri décroissant par date


#     # Regroupe par date en utilisant TruncDate et effectue les agrégations
#     orders_by_date = orders.annotate(
#         order_date=TruncDate('created_at')  # Truncate the timestamp to date
#     ).values('order_date')  # Extract the date for grouping

#     # Applique l'agrégation pour compter le nombre de commandes et la somme du montant
#     orders_by_date = orders_by_date.annotate(
#         total_orders=Count('id'),
#         total_amount=Sum('total_amount')
#     ).order_by('-order_date')  # Tri décroissant par date

#     # Pagination pour afficher 5 dates par page
#     order_paginator = Paginator(orders_by_date, 5)
#     order_page = request.GET.get('order_page')
#     try:
#         orders_by_date_page = order_paginator.page(order_page)
#     except PageNotAnInteger:
#         orders_by_date_page = order_paginator.page(1)
#     except EmptyPage:
#         orders_by_date_page = order_paginator.page(order_paginator.num_pages)

#     context = {
#         'store': store,
#         'categories': categories,
#         'products': products,
#         'paginator': paginator,
#         'category_filter': category_filter,
#         'product_name': product_name,
#         'prix_min': prix_min,
#         'prix_max': prix_max,
#         'form': form,
#         'testimonials': testimonials,
#         'testimonial_paginator': testimonial_paginator,
#         'range_10': range_10,
#         'orders_by_date': orders_by_date_page,
#         'order_date': order_date, 
#         'order_paginator': order_paginator,
#     }

#     return render(request, 'core/store_detail.html', context)

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from datetime import datetime
from .models import Store, Order
from django.contrib.auth.decorators import login_required

@login_required
def orders_by_date_detail(request, slug, order_date):
    # Récupérer le store en fonction du slug
    store = get_object_or_404(Store, slug=slug, owner=request.user)
    
    # Convertir la date reçue dans l'URL en un objet date
    order_date = datetime.strptime(order_date, "%Y-%m-%d").date()  # Conversion de la chaîne en objet date
    
    # Filtrer les commandes par date et magasin
    orders_queryset = Order.objects.filter(store=store, created_at__date=order_date, activated=True).order_by('-created_at')
    
    # Calculer le nombre total de commandes et le montant total avant la pagination
    total_orders = orders_queryset.count()  # Nombre total de commandes
    total_amount = sum(order.total_amount for order in orders_queryset)  # Calcul du montant total

    # Pagination des commandes
    paginator = Paginator(orders_queryset, 5)  # Vous pouvez ajuster le nombre de commandes par page
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    # Passer la date à l'HTML pour l'affichage
    context = {
        'store': store,
        'orders': orders,
        'total_orders': total_orders,
        'total_amount': total_amount,
        'order_date': order_date,  # Ajouter la date pour l'afficher dans le template
    }

    return render(request, 'core/orders_by_date_detail.html', context)

@login_required
def order_detail_store(request, order_id):
    # Récupérer la commande spécifique par ID
    order = get_object_or_404(Order, id=order_id)

    # Passer l'objet `order` au template
    context = {
        'order': order,
    }

    # Utilisation du nouveau template 'order_detail_store.html'
    return render(request, 'core/order_detail_store.html', context)

# @login_required
# def order_detail(request, order_id):
#     # Récupérer la commande spécifique par ID
#     order = get_object_or_404(Order, id=order_id)

#     # Passer l'objet `order` au template
#     context = {
#         'order': order,
#     }

#     return render(request, 'core/order_detail.html', context)


from django.shortcuts import render, redirect
from .models import Store, Testimonial,Testimonialproduct
from .forms import TestimonialForm,TestimonialproductForm

def add_testimonial(request, slug):
    store = Store.objects.get(slug=slug)

    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            # Créer le témoignage
            testimonial = form.save(commit=False)
            testimonial.user = request.user  # Assigner l'utilisateur connecté
            testimonial.store = store  # Assigner le magasin
            testimonial.save()
            messages.success(request, 'votre témoignage a été ajoutée avec succès.')
            return redirect('store_detail', slug=store.slug)
    else:
        form = TestimonialForm()

    return render(request, 'core/add_testimonial.html', {'form': form, 'store': store})

def add_testimonialproduct(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        form = TestimonialproductForm(request.POST)
        if form.is_valid():
            # Créer le témoignage
            testimonial = form.save(commit=False)
            testimonial.user = request.user  # Assigner l'utilisateur connecté
            testimonial.product = product  # Assigner le magasin
            testimonial.save()
            messages.success(request, 'votre témoignage a été ajoutée avec succès.')
            return redirect('product_detail', id=product.id)
    else:
        form = TestimonialproductForm()

    return render(request, 'core/add_testimonialproduct.html', {'form': form, 'product': product})




from .forms import CategoryForm
from .models import Store
from django.contrib.auth.decorators import login_required

@login_required
def create_category(request, slug):
    # Récupérer le store correspondant au slug
    store = get_object_or_404(Store, slug=slug)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Ajouter la catégorie au store
            category = form.save(commit=False)
            category.store = store
            category.save()

            # Afficher un message de succès
            messages.success(request, 'La catégorie a été ajoutée avec succès.')
            return redirect('store_detail', slug=store.slug)  # Rediriger vers la page du store
    else:
        form = CategoryForm()

    return render(request, 'core/create_category.html', {'form': form, 'store': store})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Photo, Store, Category
from .forms import ProductForm, PhotoForm

def create_product(request, slug):
    store = get_object_or_404(Store, slug=slug) 
     # Récupérer le store par son slug

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)  # Ne pas encore enregistrer dans la base
            product.store = store  # Associer le store au produit
            product.save()  # Enregistrer le produit

            # Gérer l'upload des images supplémentaires (galerie)
            images = request.FILES.getlist('image_galerie')  # Récupérer les images pour la galerie
            for img in images:
                Photo.objects.create(product=product, image=img)  # Créer des objets Photo pour chaque image

            # Message de succès
            messages.success(request, f"Le produit '{product.name}' a été ajouté avec succès au store {store.name}.")
            return redirect('store_detail', slug=store.slug) # Redirection vers la page de détail du store

    else:
        form = ProductForm()

    return render(request, 'core/create_product.html', {
        'form': form,
        'store': store,
    })

from django.shortcuts import render, get_object_or_404
from .models import Product,Testimonialproduct

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Product, Testimonialproduct

def product_detail(request, id):
    # Récupère le produit en fonction de son ID
    product = get_object_or_404(Product, id=id)

    # Récupère la catégorie du produit
    category = product.category

    # Récupère les autres produits de la même catégorie (en excluant le produit actuel)
    related_products = Product.objects.filter(category=category).exclude(id=product.id)
    
    # Récupère les témoignages associés au produit
    testimonials = Testimonialproduct.objects.filter(product=product)
    average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
    if not average_rating:
        average_rating = 0  # Si pas de témoignages, la note moyenne est 0

    # Pagination des témoignages
    paginator_testimonials = Paginator(testimonials, 3)  # 5 témoignages par page
    page_testimonials = request.GET.get('page')

    try:
        testimonials = paginator_testimonials.page(page_testimonials)
    except PageNotAnInteger:
        testimonials = paginator_testimonials.page(1)
    except EmptyPage:
        testimonials = paginator_testimonials.page(paginator_testimonials.num_pages)

    # Pagination des produits liés
    paginator_related = Paginator(related_products, 6)  # 6 produits par page
    page_related = request.GET.get('page')

    try:
        related_products = paginator_related.page(page_related)
    except PageNotAnInteger:
        related_products = paginator_related.page(1)
    except EmptyPage:
        related_products = paginator_related.page(paginator_related.num_pages)

    # Passe le produit et les produits associés au template
    return render(request, 'core/product_detail.html', {
        'product': product,
        'related_products': related_products,  # Les produits de la même catégorie
        'paginator_related': paginator_related,  # Pour la pagination des produits liés
        'paginator_testimonials': paginator_testimonials,  # Pour la pagination des témoignages
        'testimonials': testimonials,  # Les témoignages paginés
        'range_10': range(1, 11),
        'average_rating': average_rating, 
    })
 

@login_required
def store_sales_history(request, store_id):
    store = Store.objects.get(id=store_id, owner=request.user)
   
    # Obtenir toutes les commandes de la boutique
    orders = Order.objects.filter(store=store).order_by('-created_at') 



@login_required
def purchase_history(request):
    # Obtenir toutes les commandes de l'utilisateur connecté
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Tri par date décroissante
   
    return render(request, 'shop/purchase_history.html', {'orders': orders})

from django.shortcuts import render, get_object_or_404
from .models import Order

@login_required(login_url="signin")
def order_detail(request, order_id):
    # Récupérer la commande en fonction de l'ID
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Ajouter les éléments de la commande (OrderItem)
    order_items = order.items.all()
    
    # Contexte à passer au template
    context = {
        'order': order,
        'order_items': order_items,
    }
    
    return render(request, 'core/order_detail.html', context)


from django.shortcuts import render, redirect
from .forms import CommandeLivraisonForm
from django.contrib import messages
@login_required(login_url="signin")
def creer_commande(request):
    if request.method == 'POST':
        form = CommandeLivraisonForm(request.POST)
        if form.is_valid():
            # Sauvegarder la commande et l'associer à l'utilisateur
            commande = form.save(commit=False)
            commande.user = request.user  # Lier l'utilisateur connecté à la commande
            commande.save()
            messages.success(request, "Votre commande de livraison a été enregistrée avec succès.")
            return redirect('profile')  # Redirige vers une page de succès
        else:
            messages.error(request, "Il y a des erreurs dans votre formulaire.")
    else:
        form = CommandeLivraisonForm()

    return render(request, 'core/creer_commande.html', {'form': form})

def livraison_detail(request, commande_id):
    # Récupérer la commande en utilisant l'ID de la commande
    commande = get_object_or_404(CommandeLivraison, id=commande_id)
    
    context = {
        'commande': commande
    }
    
    return render(request, 'core/livraison_detail.html', context)

# from django.http import JsonResponse
# import json

# def cart(request):
    
#     cart = None
#     cartitems = []
    
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
#         cartitems = cart.cartitems.all()
    
#     context = {"cart":cart, "items":cartitems}
#     return render(request, "core/cart.html", context)

# # Voir la vue 'add_to_cart' existante
# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart = get_or_create_cart(request.user)

#     # Vérifier si l'article est déjà dans le panier
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     return redirect('core:cart_detail')

# # Ajoutez ceci dans la vue pour obtenir le nombre total d'articles
# def get_cart_item_count(user):
#     cart = get_or_create_cart(user)
#     return cart.get_item_count()
