from django.db import models

class ScrapedProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    normal_price = models.CharField(max_length=50)
    discount = models.CharField(max_length=20)
    link = models.URLField(max_length=500)
    description = models.TextField()
    advantage = models.TextField()
    category = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)  # ajout auto à l'enregistrement

    def __str__(self):
        return f"{self.name} ({self.discount})"
