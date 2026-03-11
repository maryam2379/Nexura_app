def cart_count(request):
    count = 0
    # On vérifie le panier même si l'utilisateur n'est pas connecté 
    # (ou garde ta condition if si tu préfères restreindre)
    cart = request.session.get('cart', {})
    
    for item in cart.values():
        if isinstance(item, dict):
            # Nouveau format : on extrait la valeur de la clé 'quantite'
            count += item.get('quantite', 0)
        else:
            # Ancien format ou sécurité : si c'est déjà un chiffre
            count += item
            
    return {'cart_count': count}