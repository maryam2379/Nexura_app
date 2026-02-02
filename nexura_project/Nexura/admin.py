from django.contrib import admin
from django.utils.html import format_html
from .models import Product

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