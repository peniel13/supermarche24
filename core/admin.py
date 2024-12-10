from django.contrib import admin
from .models import Store
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'profile_pic', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "profile_pic"),
            },
        ),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)

class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Store, StoreAdmin)

from .models import Category

# Define the Category admin class
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'store')  # Columns to display in the list view
    search_fields = ('name',)  # Enable search by name
    list_filter = ('store',)  # Allow filtering categories by store
    ordering = ('store', 'name')  # Order categories by store and name

    # You can add more customization if necessary
    # e.g., make store a read-only field for categories already created
    readonly_fields = ('store',)

# Register the Category model with the CategoryAdmin class
admin.site.register(Category, CategoryAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category,Photo
class PhotoInline(admin.TabularInline):  # Tu peux aussi utiliser StackInline si tu préfères
    model = Photo
    extra = 1  # Affiche un champ vide de formulaire supplémentaire pour ajouter une photo
    fields = ('image',) 

class ProductAdmin(admin.ModelAdmin):
    # Définition des champs à afficher dans la liste des produits
    list_display = ('name', 'category', 'price', 'stock', 'image_tag', 'created_at')

    # Filtres dans l'interface d'administration
    list_filter = ('category', 'price', 'stock', 'created_at')

    # Recherche par nom de produit, catégorie, prix, etc.
    search_fields = ['name', 'category__name', 'price','store',]

    # Ajout d'un inline pour afficher les photos associées
    # Vous pouvez ajouter un Inline si vous avez un modèle Photo pour les produits
    inlines = [PhotoInline]

    # Méthode pour afficher l'image du produit dans l'admin
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Pas d'image"
    
    image_tag.short_description = 'Image'

    # Optionnel : Méthode pour afficher la catégorie de manière lisible
    def get_category(self, obj):
        return obj.category.name if obj.category else "Non définie"
    get_category.short_description = 'Catégorie'

# Enregistrer le modèle et son administration
admin.site.register(Product, ProductAdmin)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'uploaded_at')
    search_fields = ('product',)
    list_filter = ('product',)

# Enregistrer les modèles dans l'admin
admin.site.register(Photo, PhotoAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Product

# Admin pour Cart
from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    # Colonnes affichées dans l'admin
    list_display = ('user', 'created_at', 'total_with_commission', 'item_count', 'is_ordered','is_active')

    # Filtres disponibles dans l'admin
    list_filter = ('created_at', 'user', 'is_ordered','is_active')  # Ajoutez 'is_ordered' pour filtrer

    # Recherche dans l'admin par nom d'utilisateur
    search_fields = ('user__username',)

    # Méthode pour afficher le total du panier avec la commission
    def total_with_commission(self, obj):
        return obj.get_total()  # Appelle la méthode get_total pour afficher le prix total + la commission

    total_with_commission.short_description = 'Total avec commission'  # Nom de la colonne

    # Méthode pour afficher le nombre d'articles dans le panier
    def item_count(self, obj):
        return obj.get_item_count()  # Appelle la méthode get_item_count pour afficher le nombre d'articles

    item_count.short_description = 'Nombre d\'articles'

# Enregistrer le modèle CartAdmin
admin.site.register(Cart, CartAdmin)



# Admin pour CartItem
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'total_price')  # Colonnes affichées
    list_filter = ('cart', 'product')  # Filtres dans l'admin
    search_fields = ('product__name', 'cart__user__username')  # Recherche par produit et utilisateur

    # Méthode pour afficher le prix total d'un article dans le panier
    def total_price(self, obj):
        return obj.get_total_price()  # Appelle la méthode get_total_price du modèle CartItem pour afficher le prix total

    total_price.short_description = 'Prix total'

# Enregistrer le modèle CartItemAdmin
admin.site.register(CartItem, CartItemAdmin)


from .models import Testimonial,Testimonialproduct

class TestimonialAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la liste d'administration
    list_display = ('store', 'user', 'rating', 'created_at', 'content_snippet')

    # Ajout d'un filtre pour la date de création
    list_filter = ('created_at', 'rating')

    # Ajout d'une barre de recherche (par exemple par le nom de l'utilisateur ou le contenu)
    search_fields = ('user__username', 'content')

    # Ajout d'une fonctionnalité pour trier les témoignages
    ordering = ('-created_at',)

    # Raccourcir l'affichage du contenu (pour ne pas afficher tout le texte dans la liste)
    def content_snippet(self, obj):
        # Limite le texte à 100 caractères
        return obj.content[:100] + '...'
    content_snippet.short_description = 'Extrait du témoignage'

    # Personnaliser le formulaire dans l'admin
    fieldsets = (
        (None, {
            'fields': ('store', 'user', 'content', 'rating')
        }),
        ('Informations supplémentaires', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # Rendre le champ 'created_at' en lecture seule
    readonly_fields = ('created_at',)

# Enregistrement de l'admin
admin.site.register(Testimonial, TestimonialAdmin)


class TestimonialproductAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la liste d'administration
    list_display = ('product', 'user', 'rating', 'created_at', 'content_snippet')

    # Ajout d'un filtre pour la date de création
    list_filter = ('created_at', 'rating')

    # Ajout d'une barre de recherche (par exemple par le nom de l'utilisateur ou le contenu)
    search_fields = ('user__username', 'content')

    # Ajout d'une fonctionnalité pour trier les témoignages
    ordering = ('-created_at',)

    # Raccourcir l'affichage du contenu (pour ne pas afficher tout le texte dans la liste)
    def content_snippet(self, obj):
        # Limite le texte à 100 caractères
        return obj.content[:100] + '...'
    content_snippet.short_description = 'Extrait du témoignage'

    # Personnaliser le formulaire dans l'admin
    fieldsets = (
        (None, {
            'fields': ('product', 'user', 'content', 'rating')
        }),
        ('Informations supplémentaires', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # Rendre le champ 'created_at' en lecture seule
    readonly_fields = ('created_at',)

# Enregistrement de l'admin
admin.site.register(Testimonialproduct, TestimonialproductAdmin)

from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html

# Classe d'administration pour OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Nombre d'éléments vides à ajouter par défaut
    readonly_fields = ('product', 'quantity', 'price_at_time_of_order', 'get_total_price')

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total'

from django.contrib import admin
from .models import Order, OrderItem
from django.utils.translation import gettext_lazy as _

class OrderAdmin(admin.ModelAdmin):
    # Affichage des champs dans l'admin
    list_display = ('id', 'user', 'store', 'status', 'activated', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('status', 'store', 'created_at', 'activated')  # Ajout de 'activated' dans les filtres
    search_fields = ('user__username', 'store__name', 'status')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    # Affichage des articles de la commande sous forme de sous-table (inline)
    inlines = [OrderItemInline]

    # Actions personnalisées pour l'admin
    actions = ['mark_as_shipped', 'calculate_total', 'activate_order']

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, _("Les commandes ont été marquées comme expédiées."))
    mark_as_shipped.short_description = _("Marquer comme expédiée")

    def calculate_total(self, request, queryset):
        for order in queryset:
            order.calculate_total()
        self.message_user(request, _("Les montants totaux ont été recalculés."))
    calculate_total.short_description = _("Calculer le montant total")

    def activate_order(self, request, queryset):
        # Activer la commande pour Mobile Money (passage de activated=False à activated=True)
        queryset.update(activated=True)
        self.message_user(request, _("Les commandes ont été activées."))
    activate_order.short_description = _("Activer les commandes Mobile Money")

    def save_model(self, request, obj, form, change):
        # Appel de la méthode parent pour sauver l'objet
        super().save_model(request, obj, form, change)

# Enregistrement des modèles dans l'admin
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import MobileMoneyPayment, Cart, Order, OrderItem
from .utils import get_or_create_cart  # Assurez-vous d'importer votre méthode pour récupérer/Créer le panier
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib import admin
from .models import MobileMoneyPayment
from .models import Cart, Order, OrderItem
# admin.py
class MobileMoneyPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_number', 'transaction_id', 'first_name', 'last_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_number', 'user__username', 'transaction_id')
    actions = ['validate_payment']

    def validate_payment(self, request, queryset):
        # Marquer les paiements comme validés
        queryset.update(status='validated')

        # Créer la commande pour chaque paiement validé
        for payment in queryset:
            cart = get_or_create_cart(payment.user)
            order = Order.objects.create(
                user=payment.user,
                store=cart.items.first().product.store,
                status='paid',
            )

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_at_time_of_order=cart_item.product.price
                )

            order.calculate_total()  # Mettre à jour le total de la commande
            cart.items.all().delete()  # Vider le panier

        self.message_user(request, "Les paiements ont été validés et les commandes ont été créées.")

    validate_payment.short_description = "Valider les paiements et créer les commandes"

# Enregistrer l'admin pour MobileMoneyPayment
admin.site.register(MobileMoneyPayment, MobileMoneyPaymentAdmin)

from django.contrib import admin
from .models import CommandeLivraison

class CommandeLivraisonAdmin(admin.ModelAdmin):
    # Afficher les champs dans la liste de l'admin
    list_display = ('nom', 'prenom', 'email', 'numero_tel', 'numero_id_colis', 'statut', 'date_commande', 'user')
    
    # Ajouter des filtres par statut, utilisateur et date
    list_filter = ('statut', 'user', 'date_commande')
    
    # Recherche par nom, email, numéro ID colis
    search_fields = ('nom', 'prenom', 'email', 'numero_id_colis')
    
    # Permettre de modifier les champs directement depuis la liste des objets
    list_editable = ('statut',)
    
    # Afficher les détails dans la vue d'édition
    fieldsets = (
        (None, {
            'fields': ('nom', 'prenom', 'email', 'numero_tel', 'user')
        }),
        ('Détails de la livraison', {
            'fields': ('adresse_livraison', 'description_colis', 'endroit_recuperation', 'numero_id_colis')
        }),
        ('Statut et dates', {
            'fields': ('statut', 'date_commande')
        }),
    )
    
    # Empêcher la modification de la date de commande
    readonly_fields = ('date_commande',)
    
    # Tris par défaut sur la date de commande (tri par date décroissante)
    ordering = ('-date_commande',)
    
    # Ajouter un bouton pour changer de statut rapidement
    actions = ['marquer_comme_livree']

    def marquer_comme_livree(self, request, queryset):
        """Action pour marquer la commande comme livrée."""
        queryset.update(statut='livree')
    marquer_comme_livree.short_description = "Marquer comme livrée"

# Enregistrer le modèle et son admin
admin.site.register( CommandeLivraison, CommandeLivraisonAdmin)

# from django.contrib import admin
# from .models import MobileMoneyTransaction

# @admin.register(MobileMoneyTransaction)
# class MobileMoneyTransactionAdmin(admin.ModelAdmin):
#     list_display = ('order', 'transaction_id', 'mobile_money_number', 'amount', 'is_verified', 'verified_at')
#     list_filter = ('is_verified', 'verified_at')
#     search_fields = ('transaction_id', 'mobile_money_number', 'order__id')
#     readonly_fields = ('transaction_id', 'mobile_money_number', 'amount', 'verified_at')

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         # Filtrer les transactions en attente de vérification
#         return queryset.filter(is_verified=False)



# Inline pour afficher les articles de commande sous la commande

