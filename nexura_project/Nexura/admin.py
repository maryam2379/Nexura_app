from django.contrib import admin
from django.utils.html import format_html
from .models import Product
from .models import Product, Commande, CommandeItem
from .models import Newsletter

# 1. Personnalisation globale des titres de l'admin
admin.site.site_header = "NEXURA - GESTION LUXE"
admin.site.site_title = "Nexura Admin Portal"
admin.site.index_title = "Tableau de bord Collection"

# 2. Une seule classe d'administration pour Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste (avec l'aperçu image)
    list_display = ('apercu_image', 'name', 'category', 'price', 'created_at')

    # Filtres latéraux
    list_filter = ('category', 'created_at')

    # Barre de recherche
    search_fields = ('name', 'category')

    # Fonction pour afficher la miniature de l'image
    def apercu_image(self, obj):
        if obj.image_front:
            return format_html('<img src="{}" style="width: 50px; height: 65px; object-fit: cover; border-radius: 3px;" />', obj.image_front.url)
        return "Aucune image"
    apercu_image.short_description = 'Visuel'

    # Fonction pour afficher une alerte visuelle sur le stock
    def stock_status(self, obj):
        if obj.stock <= 0:
            return "❌ Rupture"
        elif obj.stock <= 5:
            return "⚠️ Stock Faible"
        return "✅ En Stock"
    
    stock_status.short_description = 'État du Stock'
# Permet d'afficher les articles directement dans la vue de la commande
class CommandeItemInline(admin.TabularInline):
    model = CommandeItem
    extra = 0 # Empêche l'affichage de lignes vides inutiles
    readonly_fields = ('product', 'quantite', 'prix_unitaire') # Sécurité pour l'admin

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste principale
    list_display = ('id', 'user', 'total', 'statut', 'date_commande')
    
    # Filtres sur le côté droit
    list_filter = ('statut', 'date_commande')
    
    # Barre de recherche (par nom d'utilisateur ou ID de commande)
    search_fields = ('user__username', 'id')
    
    # Intégration des articles de la commande
    inlines = [CommandeItemInline]
    
    # Possibilité de modifier le statut rapidement depuis la liste
    list_editable = ('statut',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    # Liste des colonnes affichées dans l'interface
    list_display = ('email', 'date_inscription')
    
    # Ajout d'une barre de recherche par email
    search_fields = ('email',)
    
    # Filtre latéral pour trier par date
    list_filter = ('date_inscription',)
    
    # Tri par défaut (du plus récent au plus ancien)
    ordering = ('-date_inscription',)

    # Optionnel : Empêcher la modification d'un email déjà inscrit pour garder l'intégrité
    def has_change_permission(self, request, obj=None):
        return False