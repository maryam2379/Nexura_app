from django.urls import path
from .import views


urlpatterns = [
    path('',views.Home,name='home'),
    path('boutique/',views.boutique,name='boutique'),
    path('produit/<int:pk>/', views.detail_article, name='detail_article'),
    path('collection/',views.collection,name='collection'),
    path('apropos/',views.about,name="about"),
    path('ajouter-au-panier/<int:product_id>/', views.ajouter_au_panier, name='ajouterpanier'),
    path('panier/', views.voir_panier, name='panier'),
    path('inscription/', views.register_view, name='register'),
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'), 
]
