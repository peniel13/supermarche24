from django.db import models




class WebsiteLink(models.Model):
    # Champ pour l'image de profil
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Champ pour le nom
    name = models.CharField(max_length=100)
    
    # Champ pour ajouter un lien vers un site web
    website_link = models.URLField(max_length=200, null=True, blank=True)
    
    # Champ pour la description
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name