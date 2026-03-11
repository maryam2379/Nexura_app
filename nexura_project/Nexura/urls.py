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
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('valider-commande/', views.valider_commande, name='valider_commande'),
    path('commande/<int:commande_id>/', views.detail_commande, name='detail_commande'),
    path('commande/<int:commande_id>/pdf/', views.generer_facture_pdf, name='facture_pdf'),
    path('commande/<int:commande_id>/annuler/', views.annuler_commande, name='annuler_commande'),
    path('profil/', views.profil_view, name='profil'),
    path('suivi-commande/', views.suivi_commande_view, name='suivi_commande'),
    path('retours-echanges/', views.retours_view, name='retours_view'),
    path('guide-des-tailles/', views.guide_tailles_view, name='guide_tailles'),
    path('faq/', views.faq_view, name='faq'),
    path('newsletter-subscribe/', views.inscription_newsletter, name='newsletter_subscribe'),
]
