from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from django.contrib import messages
from payment.forms import ShippingForm
from payment.models import ShippingAdress, Order, Order_item
from dryWashing.models import Clothes, Profile
from django.contrib.auth.models import User
from register.views import update_info
import datetime
from django.http import JsonResponse
from .models import Order


def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def billing_info(request):
    # Récupérer les données de la session
    shipping_info = request.session.get('shipping_info', {})

    if request.method == "GET":
        cart = Cart(request)
        cart_clothes = cart.get_cloths()
        quantities = cart.get_quants()  
        totals = cart.cart_total()

        return render(request, "payment/billing_info.html", {
            "cart_clothes": cart_clothes,
            "quantities": quantities,
            "totals": totals,
            "shipping_info": shipping_info
        })
    else:
        messages.error(request, "Access Denied")
        return redirect('update_info')

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_clothes = cart.get_cloths()
        quantities = cart.get_quants()  
        totals = cart.cart_total()
        payment_form = ShippingForm(request.POST or None)
        my_shipping = request.session.get('shipping_info')

        if not my_shipping:  # Vérifier si la session contient les infos de livraison
            messages.error(request, "Votre session a expiré. Veuillez remplir les informations de livraison à nouveau.")
            return redirect('billing_info')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_codePostal']}"
        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, status="LINGE_RECU")
            create_order.save()

            for clothes in cart_clothes:
                clothes_id = clothes.id
                price = clothes.price
                for key, value in quantities.items():
                    if int(key) == clothes.id:
                        Order_item.objects.create(order=create_order, clothes_id=clothes_id, user=user, quantity=value, price=price)

            # Supprimer le panier de la session
            if "session_key" in request.session:
                del request.session["session_key"]

            # Supprimer le panier de la base de données
            Profile.objects.filter(user__id=request.user.id).update(old_cart="")

            messages.success(request, "Commande passée avec succès ! Suivez son état.")
            return redirect('order_status', order_id=create_order.id)
        
        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, status="LINGE_RECU")
            create_order.save()
            messages.success(request, "Commande passée avec succès ! Suivez son état.")
            return redirect('order_status', order_id=create_order.id)

    else:
        messages.error(request, "Accès refusé")
        return redirect('billing_info')

def order_status(request):
    if request.user.is_authenticated:
        # Récupère les commandes non livrées de l'utilisateur connecté
        user_orders = Order.objects.filter(user=request.user, delivered=False)
        return render(request, 'payment/order_status.html', {'orders': user_orders})
    else:
        # Redirige vers login si non connecté
        return redirect("login")
    
def get_orders_status(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).values("id", "status")
        return JsonResponse({"orders": list(orders)})
    else:
        return JsonResponse({"error": "Utilisateur non authentifié"}, status=403)
     
def delivered_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(delivered=True)
        if request.POST:
            status = request.POST['delivered-status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            # update the status
            now = datetime.datetime.now()
            order.update(delivered=False)
        
            return redirect('home')    
        return render(request, "payment/delivered_dash.html", {"orders":orders})
    else:
        messages.success(request, "commande passée")
        return redirect('home')

def not_delivered_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(delivered=False)
        
        if request.method == "POST":
            status = request.POST.get('status')
            num = request.POST.get('num')
            order = Order.objects.filter(id=num)

            # Mise à jour du statut
            if order.exists():
                order.update(status=status)
            
            return redirect('not_delivered_dash')  # On reste sur la même page après la modification
        
        return render(request, "payment/not_delivered_dash.html", {"orders": orders})
    
    else:
        messages.error(request, "Accès refusé")
        return redirect('home')
    
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # get the order
        order = Order.objects.get(id=pk)
        # get the order item
        items = Order_item.objects.filter(order=pk)

        if request.POST:
            status = request.POST['delivered-status']
            # check if true or false
            if status == "true":
                # get the order 
                order = Order.objects.filter(id=pk)
                # update the status
                now = datetime.datetime.now()
                order.update(delivered=True, date_delivered=now)
            else:
                # get the order 
                order = Order.objects.filter(id=pk)
                # update the status
                order.update(delivered=False)
            return redirect('home')

        return render(request, 'payment/orders.html', {"order":order, "items":items})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')
