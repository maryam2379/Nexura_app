# ⚜️ Nexura – E-Commerce de Mode de Luxe

**Nexura** est une plateforme e-commerce haut de gamme développée avec **Django**. Elle offre une expérience utilisateur raffinée, alliant esthétique minimaliste et fonctionnalités robustes pour la vente d'articles de luxe.

---

## ✨ Fonctionnalités

- **Boutique Élégante** : Grille de produits avec affichage dynamique et effets de survol (hover) sur les visuels.
- **Panier Dynamique** : Gestion du panier via les sessions Django avec un compteur d'articles en temps réel dans la barre de navigation.
- **Filtrage Avancé** : Système de tri par catégorie et par prix (intégré en JavaScript pour la fluidité).
- **Espace Membre Privilégié** : 
  - Authentification sécurisée (Connexion/Déconnexion).
  - Inscription personnalisée incluant l'adresse de livraison et le téléphone.
  - Restriction d'achat : seuls les membres connectés peuvent ajouter des articles au panier.
- **Gestion Médias** : Automatisation du stockage et de l'affichage des images produits.

---

## 🛠️ Stack Technique

- **Framework :** [Django 3 Flash variant](https://www.djangoproject.com/) (Python 3.10+)
- **Frontend :** HTML5, CSS3 (Design Custom Noir & Or), JavaScript (ES6+), Bootstrap 5.
- **Base de données :** SQLite (Développement).
- **Outils :** Pillow (Traitement d'images), FontAwesome (Iconographie).



---

## 🚀 Installation Rapide

1. **Clonage du dépôt :**
   ```bash
   git clone [https://github.com/votre-username/nexura.git](https://github.com/votre-username/nexura.git)
   cd nexura
2. **Configuration de l'environnement :**
    ```Bash

    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install django pillow

3. **Migrations et Base de données :**
    ```Bash

    python manage.py makemigrations
    python manage.py migrate

4. **Lancement du serveur :**
    ```Bash

    python manage.py runserver

    Accédez à l'application sur : http://127.0.0.1:8000

## 📁 Structure du Projet

    Nexura/ : Cœur de l'application (Vues, Modèles, Context Processors).

    nexura_project/ : Configuration globale et gestion des URLs.

    media/ : Répertoire de stockage des visuels produits.

    templates/ : Architecture des pages HTML (Boutique, Panier, Profil, Auth).

## 🎨 Identité Visuelle
Élément	Couleur / Style
Fond Principal	#0a0a0a (Noir Onyx)
Accents	#D4AF37 (Or Nexura)
Typographie	Serif (Élégance classique)

Développé par [Mar'yam Mfopit/Skydev] Nexura – L'élégance à portée de clic.
