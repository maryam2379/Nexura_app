from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, FileResponse
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .forms import ExtendedRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.db.models import Q

# Imports des modèles et formulaires locaux
from .models import Commande, CommandeItem, Newsletter, Product
from .forms import ExtendedRegisterForm, ProfileUpdateForm

# Imports techniques pour le PDF
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# --- FONCTIONS UTILITAIRES ---

def generer_pdf_buffer(commande):
    """Génère le contenu binaire du PDF pour réutilisation (vue et email)"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Design de la facture
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "NEXURA LUXE")
    p.setStrokeColor(colors.HexColor("#D4AF37"))
    p.line(50, height - 65, width - 50, height - 65)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 100, f"FACTURE : #NX-{commande.id}")
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 115, f"Date : {commande.date_commande.strftime('%d/%m/%Y')}")
    p.drawString(50, height - 130, f"Client : {commande.user.username}")
    
    y = height - 180
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Produit")
    p.drawString(300, y, "Qté")
    p.drawString(500, y, "Total")
    p.line(50, y - 5, width - 50, y - 5)
    
    y -= 25
    p.setFont("Helvetica", 10)
    for item in commande.items.all():
        p.drawString(50, y, f"{item.product.name}")
        p.drawString(305, y, f"{item.quantite}")
        p.drawString(505, y, f"{item.total_item} €")
        y -= 20

    p.setFont("Helvetica-Bold", 12)
    p.drawString(350, y - 20, f"TOTAL TTC : {commande.total} €")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def envoyer_confirmation_commande(commande):
    """Prépare et envoie l'e-mail avec le PDF attaché"""
    sujet = f"Confirmation de votre commande Nexura Luxe #NX-{commande.id}"
    # Assurez-vous que le template 'emails/confirmation_commande.html' existe
    message = render_to_string('emails/confirmation_commande.html', {'commande': commande})
    
    email = EmailMessage(
        sujet,
        message,
        'noreply@nexura.com',
        [commande.user.email],
    )
    email.content_subtype = "html"

    # Attacher le PDF généré dynamiquement
    pdf_buffer = generer_pdf_buffer(commande)
    email.attach(f'Facture_Nexura_{commande.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
    
    email.send()

# --- VUES DE NAVIGATION ---

def chargement(request):
    return render(request, 'chargement.html')

def Home(request):
    return render(request, 'Home.html')

from django.utils import timezone
from datetime import timedelta

def boutique(request):
    category_name = request.GET.get('categorie')
    query = request.GET.get('q')
    filtre_special = request.GET.get('filtre') # Nouveau : pour 'nouveautes' ou 'promos'
    
    products = Product.objects.all()
    
    # --- FILTRE SPÉCIAL (FOOTER) ---
    if filtre_special == 'nouveautes':
        # Produits créés les 30 derniers jours
        un_mois_dernier = timezone.now() - timedelta(days=30)
        products = products.filter(created_at__gte=un_mois_dernier).order_by('-created_at')
    
    elif filtre_special == 'promos':
        # Si tu as un champ 'old_price' ou 'is_sale'
        # Ici on simule avec un filtre sur les prix bas ou un champ booléen
        products = products.filter(price__lt=300) # Exemple : articles à moins de 100€

    # --- RECHERCHE & CATÉGORIES (Existant) ---
    if query:
        products = products.filter(Q(name__icontains=query))
    if category_name:
        products = products.filter(category=category_name)
        
    categories = Product.CATEGORY_CHOICES 
    
    return render(request, 'boutique.html', {
        'products': products,
        'categories': categories,
        'active_category': category_name,
        'query': query
    })

def detail_article(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'detail_article.html', {'product': product})

def collection(request):
    return render(request, 'collection.html')

def about(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')
        try:
            send_mail(
                f'Nouveau message Nexura de {name}',
                f'De: {email}\n\nMessage:\n{message_content}',
                'votre-email@gmail.com',
                ['votre-email@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Votre message a été transmis avec élégance.")
        except Exception:
            messages.error(request, "Une erreur technique est survenue.")
        return redirect('about')
    return render(request, 'about.html')

# --- GESTION DU PANIER ---

def ajouter_au_panier(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Une connexion est requise pour accéder au panier.")
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    # Correction : On utilise systématiquement le format dictionnaire pour éviter les erreurs de type
    product_key = str(product_id)
    if product_key in cart:
        if isinstance(cart[product_key], dict):
            cart[product_key]['quantite'] += 1
        else:
            # Migration de l'ancien format vers le nouveau si nécessaire
            cart[product_key] = {'quantite': cart[product_key] + 1, 'prix': str(product.price)}
    else:
        cart[product_key] = {'quantite': 1, 'prix': str(product.price)}
    
    request.session['cart'] = cart
    messages.success(request, f"{product.name} ajouté à votre sélection.")
    return redirect('boutique')

def voir_panier(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=product_id)
        # Extraction sécurisée de la quantité qu'elle soit un dict ou un int
        qty = item_data['quantite'] if isinstance(item_data, dict) else item_data
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
    
    return render(request, 'panier.html', {'cart_items': cart_items, 'total': total})

# --- AUTHENTIFICATION ---

def register_view(request):
    if request.method == "POST":
        form = ExtendedRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bienvenue chez Nexura, votre compte a été créé.")
            return redirect('home')
    else:
        form = ExtendedRegisterForm()
    return render(request, 'login&register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login&register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- COMMANDES ET DASHBOARD ---

@login_required
def dashboard_view(request):
    commandes = Commande.objects.filter(user=request.user).order_by('-date_commande')
    return render(request, 'dashboard.html', {'commandes': commandes})
@login_required
def valider_commande(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Votre panier est vide.")
        return redirect('boutique')

    # 1. Vérification préalable des stocks
    for product_id, item_data in cart.items():
        produit = get_object_or_404(Product, id=product_id)
        qty = item_data['quantite'] if isinstance(item_data, dict) else item_data
        if produit.stock < qty:
            messages.error(request, f"Désolé, le produit {produit.name} n'est plus disponible en quantité suffisante (Stock : {produit.stock}).")
            return redirect('voir_panier')

    # 2. Créer la commande
    nouvelle_commande = Commande.objects.create(
        user=request.user,
        total=0,
        adresse_livraison="Adresse de test", 
        statut='En attente'
    )

    total_general = 0
    for product_id, item_data in cart.items():
        produit = Product.objects.get(id=product_id)
        qty = item_data['quantite'] if isinstance(item_data, dict) else item_data
        
        # 3. Mise à jour du stock
        produit.stock -= qty
        produit.save()

        prix = float(produit.price)
        CommandeItem.objects.create(
            commande=nouvelle_commande,
            product=produit,
            quantite=qty,
            prix_unitaire=prix
        )
        total_general += prix * qty

    nouvelle_commande.total = total_general
    nouvelle_commande.save()
    
    # Envoi de l'email et vidage du panier
    try:
        envoyer_confirmation_commande(nouvelle_commande)
    except Exception as e:
        print(f"Erreur mail: {e}")

    request.session['cart'] = {}
    messages.success(request, "Commande validée et stocks mis à jour !")
    return redirect('dashboard')

@login_required
def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, user=request.user)
    return render(request, 'detail_commande.html', {'commande': commande, 'items': commande.items.all()})

@login_required
def generer_facture_pdf(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, user=request.user)
    buffer = generer_pdf_buffer(commande)
    return FileResponse(buffer, as_attachment=True, filename=f"Facture_Nexura_{commande.id}.pdf")

@login_required
def annuler_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, user=request.user, statut='En attente')
    commande.statut = 'Annulée'
    commande.save()
    messages.success(request, f"La commande #NX-{commande.id} a été annulée.")
    return redirect('dashboard')

@login_required
def profil_view(request):
    # --- AJOUT DE CETTE SÉCURITÉ ---
    # Si l'utilisateur n'a pas de profil, on le crée à la volée
    if not hasattr(request.user, 'profile'):
        from .models import Profile
        Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Votre profil Nexura a été mis à jour.")
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'profil.html', {
        'u_form': u_form,
        'p_form': p_form
    })

def suivi_commande_view(request):
    commande = None
    if request.method == "POST":
        order_input = request.POST.get('order_id').replace('NX-', '').strip()
        email_input = request.POST.get('email').strip()

        try:
            # On cherche la commande qui correspond à l'ID et à l'email du compte
            commande = Commande.objects.get(id=order_input, user__email=email_input)
        except (Commande.DoesNotExist, ValueError):
            messages.error(request, "Aucune commande trouvée avec ces informations.")
            
    return render(request, 'suivi_commande.html', {'commande': commande})

def retours_view(request):
    return render(request, 'retours.html')

def guide_tailles_view(request):
    return render(request, 'Guide_Tailles.html')

def faq_view(request):
    return render(request, 'faq.html')

def inscription_newsletter(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            # On vérifie si l'email existe déjà pour éviter les doublons
            if not Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.create(email=email)
                messages.success(request, "Bienvenue dans l'univers Nexura !")
            else:
                messages.info(request, "Vous faites déjà partie de nos membres privilégiés.")
    
    # Redirige l'utilisateur là où il était (Home, Boutique, etc.)
    return redirect(request.META.get('HTTP_REFERER', 'home'))