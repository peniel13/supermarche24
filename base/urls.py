from django.urls import path
from .import views

urlpatterns= [
    path('',views.index, name= 'index'),
    path('list_product/',views.list_product, name= 'list_product'),
    path('list_store/',views.list_store, name= 'list_store'),
    path('contact/', views.contact, name='contact'),
    path('apropos/', views.apropos, name='apropos'),
    
]