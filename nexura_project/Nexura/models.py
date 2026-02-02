from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    
    # Correction : "decimal_places" au lieu de "decimal_name"
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (€)")
    
    image_front = models.ImageField(upload_to='products/front/', verbose_name="Image de face")
    image_back = models.ImageField(upload_to='products/back/', verbose_name="Image au survol (hover)")
    
    CATEGORY_CHOICES = [
        ('VESTE', 'Vestes'),
        ('MANTEAU', 'Manteaux'),
        ('ACCESSOIRE', 'Accessoires'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='VESTE')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produit"
        ordering = ['-created_at']