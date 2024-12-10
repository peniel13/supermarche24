from django.shortcuts import render,redirect
from core.models import Store, Category, Product
from .models import WebsiteLink

# Create your views here.

def index(request):
    # Récupérer les 3 derniers magasins
    stores = Store.objects.all().order_by('-created_at')[:3]
    

    # Calculer la note moyenne de chaque store à l'aide d'agrégation
    for store in stores:
        testimonials = Testimonial.objects.filter(store=store)
        if testimonials.exists():
            store.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
        else:
            store.average_rating = 0

    # Récupérer les 3 derniers produits
    products = Product.objects.all().order_by('-created_at')[:3]

    # Calculer la note moyenne de chaque produit à l'aide d'agrégation
    for product in products:
        testimonials = Testimonialproduct.objects.filter(product=product)  # Récupère les témoignages associés
        if testimonials.exists():
            product.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
        else:
            product.average_rating = 0

    # Récupérer les liens des sites web et implémenter la recherche
    websites = WebsiteLink.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        websites = websites.filter(name__icontains=search_query) | websites.filter(description__icontains=search_query)

    # Pagination des WebsiteLinks
    paginator = Paginator(websites, 3)  # 3 WebsiteLinks par page
    page = request.GET.get('page')

    try:
        websites = paginator.page(page)
    except PageNotAnInteger:
        websites = paginator.page(1)
    except EmptyPage:
        websites = paginator.page(paginator.num_pages)

    # Passer toutes les données nécessaires au template
    return render(request, "base/index.html", {  
        'stores': stores,  # Liste des 3 derniers magasins
        'products': products,  # Liste des 3 derniers produits
        'websites': websites,  # Liens des sites web avec pagination
        'paginator': paginator,  # Paginator pour la pagination des WebsiteLinks
        'rating_choices': Testimonial.RATING_CHOICES,  # Options de note pour les témoignages
        'range_10': range(1, 11),  # Plage des étoiles pour l'affichage des notes
    })

def apropos(request):
    return render(request,'base/apropos.html')

def contact(request):
    return render(request,'base/contact.html')

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum

from django.contrib.auth.decorators import login_required

from django.db.models import Avg
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from core.models import Product, Category, Testimonialproduct  # Assurez-vous d'importer les bons modèles

def list_product(request):
    # Récupère tous les produits de tous les magasins
    products = Product.objects.all().order_by('-created_at')

    # Filtrage par catégorie
    category_filter = request.GET.get('categorie', '')
    if category_filter:
        products = products.filter(category__id=category_filter)

    # Filtrage par nom
    product_name = request.GET.get('nom', '')
    if product_name:
        products = products.filter(name__icontains=product_name)

    # Filtrage par prix
    prix_min = request.GET.get('prix_min', '')
    prix_max = request.GET.get('prix_max', '')
    if prix_min:
        try:
            prix_min = float(prix_min)
            products = products.filter(price__gte=prix_min)
        except ValueError:
            pass  # Ignore les valeurs incorrectes
    if prix_max:
        try:
            prix_max = float(prix_max)
            products = products.filter(price__lte=prix_max)
        except ValueError:
            pass  # Ignore les valeurs incorrectes

    # Calcul de la moyenne des ratings pour chaque produit
    for product in products:
        testimonials = Testimonialproduct.objects.filter(product=product)  # Récupère les témoignages associés
        if testimonials.exists():
            product.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
        else:
            product.average_rating = 0

    # Filtrage par rating
    min_rating = request.GET.get('rating_min', '')
    if min_rating:
        try:
            min_rating = float(min_rating)
            products = products.filter(average_rating__gte=min_rating)
        except ValueError:
            pass  # Ignore les valeurs incorrectes

    # Pagination
    paginator = Paginator(products, 6)  # 6 produits par page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Récupère toutes les catégories pour le filtrage
    categories = Category.objects.all()

    # Plage de 1 à 10 pour les étoiles de rating
    range_10 = range(1, 11)

    context = {
        'products': products,
        'categories': categories,
        'product_name': product_name,
        'category_filter': category_filter,
        'prix_min': prix_min,
        'prix_max': prix_max,
        'min_rating': min_rating,
        'paginator': paginator,
        'range_10': range_10,  # Plage pour les étoiles
    }

    return render(request, 'base/list_product.html', context)


from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from core.models import Store, Testimonial


def list_store(request):
    stores = Store.objects.all()

    # Filtrage par nom
    store_name = request.GET.get('nom', '')
    if store_name:
        stores = stores.filter(name__icontains=store_name)

    # Filtrage par commune
    commune = request.GET.get('commune', '')
    if commune:
        stores = stores.filter(commune=commune)

    # Pagination - 4 stores par page
    paginator = Paginator(stores, 4)
    page_number = request.GET.get('page')

    try:
        stores_page = paginator.page(page_number)
    except PageNotAnInteger:
        stores_page = paginator.page(1)
    except EmptyPage:
        stores_page = paginator.page(paginator.num_pages)

    # Calcul de la note moyenne de chaque store à l'aide d'agrégation
    for store in stores_page:
        testimonials = Testimonial.objects.filter(store=store)
        if testimonials.exists():
            store.average_rating = testimonials.aggregate(Avg('rating'))['rating__avg']
        else:
            store.average_rating = 0
    communes = [
    ('', 'Toutes les communes'),
    ('ngaliema', 'Ngaliema'),
    ('limete', 'Limete'),
    ('mongafula', 'Mongafula'),
    ('kingabwa', 'Kingabwa'),
    ('bandalungwa', 'Bandalungwa'),
    ('kinshasa', 'Kinshasa'),
    ('gombe', 'Gombe'),
    ('kasa-vubu', 'Kasa-Vubu'),
    ('ngiri-ngiri', 'Ngiri-Ngiri'),
    ('kinkole', 'Kinkole'),
    ('matete', 'Matete'),
    ('kinshasa', 'Kinshasa'),
    ('kimbanguiste', 'Kimbanguiste'),
    ('kalamu', 'Kalamu'),
    ('ngaba', 'Ngaba'),
    ('lemba', 'Lemba'),
    ('madrassah', 'Madrassah'),
    ('masina', 'Masina'),
    ('lualaba', 'Lualaba'),
    ('kwa-kabuya', 'Kwa-Kabuya'),
    ('makala', 'Makala'),
    ('bumbu', 'Bumbu'),
    ('ngombé', 'Ngombé'),
    ('eala', 'Eala'),
]
    context = {
        'stores': stores_page,
        'store_name': store_name,
        'rating_choices': Testimonial.RATING_CHOICES,
        'range_10': range(1, 11),  # Créer la plage de 1 à 10 pour les étoiles
        'communes': communes,
        'commune': commune,
    }

    return render(request, "base/list_store.html", context)


