from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from Nexura.models import Product
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required



# Create your views here.
def chargement(request):
    return render (request,'chargement.html')

def Home(request):
    return render(request,'Home.html')

def boutique(request):
    products = Product.objects.all()
    return render(request, 'boutique.html', {'products': products})

# Nouvelle vue pour le détail
def detail_article(request, pk):
    # Récupère le produit par sa clé primaire (pk)
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'detail_article.html', {'product': product})

def collection(request):
    return render(request,'collection.html' )

def about(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')

        try:
            send_mail(
                f'Nouveau message Nexura de {name}',
                f'De: {email}\n\nMessage:\n{message_content}',
                'maryamfopit@gmail.com',
                ['maryamfopit@gmail.com'],
                fail_silently=False,
            )
            # On ajoute le message de succès ici
            messages.success(request, "Votre message a été transmis avec élégance.")
        except Exception:
            messages.error(request, "Une erreur technique est survenue.")
            
        return redirect('about')
    return render (request,'about.html')

def ajouter_au_panier(request, product_id):
    # 1. Vérification de connexion
    if not request.user.is_authenticated:
        messages.warning(request, "L'accès à nos collections exclusives nécessite une connexion à votre compte Nexura.")
        return redirect('login')  # Redirige vers ta page de login

    # 2. Si connecté, on récupère le produit
    product = get_object_or_404(Product, id=product_id)
    
    # Ici, ajoute ta logique habituelle pour le panier (session ou modèle Cart)
    # Exemple simplifié avec session :
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    
    messages.success(request, f"{product.name} a été ajouté à votre sélection.")
    return redirect('boutique')

def voir_panier(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    
    return render(request, 'panier.html', {
        'cart_items': cart_items,
        'total': total,
    })

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Connecte l'utilisateur après l'inscription
            messages.success(request, "Bienvenue chez Nexura, votre compte a été créé.")
            return redirect('boutique')
    else:
        form = UserCreationForm()
    return render(request, 'login&register.html', {'form': form})

# Vue de Connexion (Login)
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('boutique')
    else:
        form = AuthenticationForm()
    return render(request, 'login&register.html', {'form': form})

# Vue de Déconnexion
def logout_view(request):
    logout(request)
    return redirect('boutique')