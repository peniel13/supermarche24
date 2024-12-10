from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify # type: ignore
from decimal import Decimal

# Create your models here.


class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    
    def __str__(self):
        return self.email
# Choix pour les communes
COMMUNES_CHOICES = [
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
class Store(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stores")
    name = models.CharField(max_length=255)
    slug=models.SlugField(blank=True, null=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="img", null=True, blank=True, verbose_name="Image du Store")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    commune = models.CharField(max_length=100, choices=COMMUNES_CHOICES, default='kinshasa', verbose_name="Commune")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    RATING_CHOICES = [(i, f'{i}/10') for i in range(1, 11)]  # Créer des choix de 1 à 10

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="testimonials")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()  # Le texte du témoignage
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)  # Choix entre 1 et 10
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Testimonial for {self.store.name} by {self.user.username}'
    
    class Meta:
        ordering = ['-created_at']


class Category(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)
   
    def __str__(self):
        return self.name

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_galerie = models.ImageField(upload_to='product/galerie/', null=True, blank=True, verbose_name="Image galerie")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def get_total_price(self, quantity):
        return self.price * quantity

class Testimonialproduct(models.Model):
    RATING_CHOICES = [(i, f'{i}/10') for i in range(1, 11)]  # Créer des choix de 1 à 10

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="testimonials")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()  # Le texte du témoignage
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)  # Choix entre 1 et 10
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Testimonial for {self.store.name} by {self.user.username}'
    
    class Meta:
        ordering = ['-created_at']

class Photo(models.Model):
    product = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/galerie/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.product} - {self.image.name}"




# models.py
from django.db import models
from django.conf import settings

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True) # Ajoutez ce champ

    def __str__(self):
        return f"Panier de {self.user.username}"

    def get_total(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        commission = 5000
        return total_price + commission

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Définir un valeur par défaut de 1

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.product.price}"

    def get_total_price(self):
        return self.product.price * self.quantity


# models.py

from django.db import models
from decimal import Decimal
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50, choices=[('pending', 'En attente'), ('En attente', 'Payée'), ('shipped', 'Expédiée'),('servit', 'Servit')],
        default='pending'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    activated = models.BooleanField(default=True)  # Par défaut, l'ordre est activé
    
    def __str__(self):
        return f"Commande {self.id} - {self.store.name} - {self.status}"

    def calculate_total(self):
        """Calculer et mettre à jour le montant total de la commande"""
        self.total_amount = sum(item.get_total_price() for item in self.items.all())
        self.save()

    def get_total(self):
        """Retourner le montant total de la commande"""
        return self.total_amount


# Article de commande (Produit associé à une commande)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.price_at_time_of_order}"

    def get_total_price(self):
        # Vérifie si price_at_time_of_order et quantity ne sont pas None
        if self.price_at_time_of_order is None or self.quantity is None:
            return Decimal('0.00')  # Retourne 0 si des valeurs manquent
        return self.price_at_time_of_order * self.quantity

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)
   
#     def __str__(self):
#         return f"{self.product.name} - {self.quantity} x {self.price_at_time_of_order}"

#     def get_total_price(self):
#         return self.price_at_time_of_order * self.quantity


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# models.py
class MobileMoneyPayment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('validated', 'Validé'),
        ('rejected', 'Rejeté'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_number = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100, unique=True)  # Transaction ID unique
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    delivery_option = models.CharField(max_length=100, choices=[('home', 'A domicile'), ('pickup', 'Récupérer soi-même')])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Etat du paiement
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.transaction_id}"

    def get_total_amount(self):
        # Calculer le montant total du panier
        return sum(item.product.price * item.quantity for item in self.cart.items.all())

class CommandeLivraison(models.Model):
    # Informations du client
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    numero_tel = models.CharField(max_length=15)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Détails de la livraison
    adresse_livraison = models.TextField()
    description_colis = models.TextField()
    endroit_recuperation = models.CharField(max_length=255)
    numero_id_colis = models.CharField(max_length=100)

    # Statut de la commande
    statut = models.CharField(
        max_length=20,
        choices=[('en_attente', 'En attente'), ('en_cours', 'En cours'), ('livree', 'Livrée')],
        default='en_attente'
    )
    
    # Dates
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande {self.numero_id_colis} par {self.nom} {self.prenom}"

    class Meta:
        permissions = [
            ("peut_marquer_comme_livree", "Peut marquer les commandes comme livrées"),
        ]
