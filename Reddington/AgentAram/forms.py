from django import forms

# Choix de catégories personnalisées
PRODUCT_CHOICES = [
    ('electromenager', 'Électroménager'),
    ('tv', 'Télévision'),
    ('ordinateur', 'Ordinateur'),
    ('telephone', 'Téléphone'),
    ('tech', 'Tech (général)'),
]

class PromoForm(forms.Form):
    product_category = forms.ChoiceField(
        choices=PRODUCT_CHOICES,
        label="Catégorie de produit",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    number_of_articles = forms.IntegerField(
        label="Nombre de produits souhaités",
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    discount_threshold = forms.IntegerField(
        label="Réduction minimale (%)",
        min_value=10,
        max_value=90,
        initial=20,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

