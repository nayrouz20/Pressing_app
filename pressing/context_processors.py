from payment.models import Order

def latest_order(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user).order_by('-date_ordered').first()  # Modifier ici
        return {'latest_order': order}
    return {}
