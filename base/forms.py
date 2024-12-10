from django import forms
from .models import  WebsiteLink

class WebsiteLinkForm(forms.ModelForm):
    class Meta:
        model = WebsiteLink
        fields = ['profile_picture', 'name', 'website_link', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Rendre la zone de texte plus grande
        }

    # Optionnel: Vous pouvez ajouter des validations ou des personnalisations ici
    def clean_website_link(self):
        website_link = self.cleaned_data.get('website_link')
        if website_link and not website_link.startswith('http'):
            raise forms.ValidationError('Le lien doit commencer par "http://" ou "https://"')
        return website_link