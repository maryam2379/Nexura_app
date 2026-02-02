def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        cart = request.session.get('cart', {})
        for quantity in cart.values():
            count += quantity
    return {'cart_count': count}