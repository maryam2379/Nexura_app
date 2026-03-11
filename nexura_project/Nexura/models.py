from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    
    # Correction : "decimal_places" au lieu de "decimal_name"
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (€)")
    
    image_front = models.ImageField(upload_to='products/front/', verbose_name="Image de face")
    image_back = models.ImageField(upload_to='products/back/', verbose_name="Image au survol (hover)")
    stock = models.PositiveIntegerField(default=10)
    
    CATEGORY_CHOICES = [
        ('VESTE', 'Vestes'),
        ('MANTEAU', 'Manteaux'),
        ('ACCESSOIRE', 'Accessoires'),
        ('ROBE','Robes'),
        ('CHAUSSURE','Chaussures'),
        ('PANTALON','pantalons'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='VESTE')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produit"
        ordering = ['-created_at']


class Commande(models.Model):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('En cours', 'Préparation'),
        ('Expédiée', 'Expédiée'),
        ('Livrée', 'Livrée'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    date_commande = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='En attente')
    adresse_livraison = models.TextField()

    def __str__(self):
        return f"Commande #{self.id} - {self.user.username}"

class CommandeItem(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantite} x {self.product.name}"
    
    @property
    def total_item(self):
        return self.quantite * self.prix_unitaire
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    ville = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

# --- SIGNAUX : Crée automatiquement un profil quand un User est créé ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email: # On vérifie qu'il y a un email
        try:
            subject = "Bienvenue dans l'univers Nexura"
            message = render_to_string('emails/welcome_email.html', {'user': instance})
            
            email = EmailMessage(
                subject,
                message,
                'noreply@nexura.com',
                [instance.email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)
        except Exception as e:
            print(f"Erreur d'envoi d'email : {e}")

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __clstr__(self):
        return self.email