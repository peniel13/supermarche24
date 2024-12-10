from django import forms
from .models import Store, Category, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    email= forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email adress"}))
    username= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ["email","username","password1","password2"]

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter firstname"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter lastname"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter email address"}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter address"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Enter bio"}))
    role = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter role"}))

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "address", "bio", "phone", "role", "profile_pic"]

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description',"thumbnail", 'commune']  # Retiré le champ 'slug', car il est généré automatiquement
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez le nom du store'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez la description du store'
            }),
            'commune': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

from django import forms
from .models import Testimonial,Testimonialproduct # Assurez-vous que le modèle Testimonial est importé

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['content', 'rating']  # Le champ 'store' est exclu car il est automatiquement pris en compte
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Partagez votre témoignage'
            }),
            'rating': forms.Select(choices=Testimonial.RATING_CHOICES, attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        }

class TestimonialproductForm(forms.ModelForm):
    class Meta:
        model = Testimonialproduct
        fields = ['content', 'rating']  # Le champ 'store' est exclu car il est automatiquement pris en compte
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Partagez votre témoignage'
            }),
            'rating': forms.Select(choices=Testimonial.RATING_CHOICES, attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez le nom du store'
            }),
            }

from .models import Product,Photo,CartItem# Assurez-vous que le modèle Product est importé

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'stock', 'image', 'image_galerie']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Application du même style pour chaque champ
        self.fields['name'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez le nom du produit'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Décrivez le produit',
            'rows': 4
        })
        self.fields['price'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez le prix'
        })
        self.fields['stock'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Indiquez le stock disponible'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
        self.fields['image_galerie'].widget.attrs.update({
            'class': 'hidden',  # Cacher le champ image_galerie par défaut
        })

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })

from django import forms
from .models import Cart, CartItem

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = []  # Le modèle Cart n'a pas de champs directement modifiables via un formulaire

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Le formulaire ne manipule pas directement des champs dans Cart, 
        # mais plutôt les CartItems associés au panier
        self.fields['quantity'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Quantité'
        })


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']  # Le champ 'quantity' permet de modifier la quantité d'un produit dans le panier

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Quantité',
        })

from django import forms
from .models import MobileMoneyPayment
from django.core.exceptions import ValidationError
# forms.py
from django import forms
from .models import MobileMoneyPayment

class MobileMoneyPaymentForm(forms.ModelForm):
    class Meta:
        model = MobileMoneyPayment
        fields = ['first_name', 'last_name', 'transaction_number', 'transaction_id', 'phone_number', 'delivery_option']
    
    def clean_transaction_id(self):
        transaction_id = self.cleaned_data['transaction_id']
        if MobileMoneyPayment.objects.filter(transaction_id=transaction_id).exists():
            raise forms.ValidationError("Ce numéro de transaction a déjà été utilisé.")
        return transaction_id

from django import forms
from .models import CommandeLivraison

class CommandeLivraisonForm(forms.ModelForm):
    class Meta:
        model = CommandeLivraison
        fields = [
            'nom', 'prenom', 'email', 'numero_tel', 'adresse_livraison', 
            'description_colis', 'endroit_recuperation', 'numero_id_colis'
        ]
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez votre nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez votre prénom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez votre email'
            }),
            'numero_tel': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez votre numéro de téléphone'
            }),
            'adresse_livraison': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Entrez l\'adresse de livraison'
            }),
            'description_colis': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Description du colis'
            }),
            'endroit_recuperation': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Endroit de récupération'
            }),
            'numero_id_colis': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Numéro d\'ID du colis'
            }),
        }

    # Optionnel : Personnaliser la validation
    def clean_numero_tel(self):
        numero_tel = self.cleaned_data.get('numero_tel')
        if not numero_tel.isdigit():
            raise forms.ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
        return numero_tel

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError("Veuillez entrer un email valide.")
        return email




# class MobileMoneyPaymentForm(forms.ModelForm):
#     class Meta:
#         model = MobileMoneyPayment
#         fields = ['transaction_number', 'transaction_id', 'first_name', 'last_name']
#         widgets = {
#             'transaction_number': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#                 'placeholder': 'Numéro de transaction'
#             }),
#             'transaction_id': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#                 'placeholder': 'ID de transaction'
#             }),
#             'first_name': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#                 'placeholder': 'Prénom'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
#                 'placeholder': 'Nom'
#             }),
            
#         }

#     def clean_transaction_id(self):
#         transaction_id = self.cleaned_data['transaction_id']
#         if MobileMoneyPayment.objects.filter(transaction_id=transaction_id).exists():
#             raise ValidationError("Ce numéro de transaction a déjà été utilisé. Veuillez utiliser un numéro de transaction unique.")
#         return transaction_id


# from django import forms
# from .models import MobileMoneyTransaction

# class MobileMoneyTransactionForm(forms.ModelForm):
#     class Meta:
#         model = MobileMoneyTransaction
#         fields = ['mobile_money_number', 'transaction_id', 'amount']

#     def __init__(self, *args, **kwargs):
#         # S'assurer que le champ 'amount' est en lecture seule
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.order:
#             self.fields['amount'].initial = self.instance.order.total_amount
#             self.fields['amount'].widget.attrs['readonly'] = True

#     def clean_transaction_id(self):
#         transaction_id = self.cleaned_data.get('transaction_id')
#         if MobileMoneyTransaction.objects.filter(transaction_id=transaction_id).exists():
#             raise forms.ValidationError("Cet ID de transaction a déjà été utilisé.")
#         return transaction_id

# from django import forms
# from .models import Order, OrderItem

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['user', 'store', 'status', 'total_amount']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance:
#             self.fields['total_amount'].widget.attrs['readonly'] = True  # Montant total en lecture seule
#             self.fields['status'].widget.attrs['class'] = 'form-control'  # Appliquer un style personnalisé si besoin

# class OrderItemForm(forms.ModelForm):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'price_at_time_of_order']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance:
#             self.fields['price_at_time_of_order'].widget.attrs['readonly'] = True  # En lecture seule
