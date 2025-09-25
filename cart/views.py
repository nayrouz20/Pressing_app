from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import User, Order, CartItem, Cart
from dryWashing.serializers import UserSerializer, CartItemSerializer, CartSerializer
from django.contrib.auth.models import User
from .cart import Cart
from dryWashing.models import Clothes

"""
# Create your views here.
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        # Personnalisation de la création d'un nouveau panier
        serializer.save(user=self.request.user)  # Initialiser le panier avec l'utilisateur actuel

    @action(detail=False, methods=['GET'])
    @permission_classes([IsAuthenticated])
    def cart(self, request):
        # Logique pour afficher le panier de l'utilisateur
        user = request.user
        user_cart = Cart.objects.filter(user=user).first()
        
        if user_cart:
            serializer = CartSerializer(user_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_404_NOT_FOUND)

    @login_required
    @api_view(['POST'])
    @permission_classes([IsAdminUser])
    def validate_order(request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        if request.method == 'POST':
            action = request.data.get('action')  # Action à effectuer sur la commande (accepter ou rejeter)
            if action == 'accept':
                # Traitez ici l'acceptation de la commande
                order.status = 'SALE'  # Modification du statut de la commande
                order.save()
                return JsonResponse({'message': 'Order accepted successfully'}, status=status.HTTP_200_OK)
            elif action == 'reject':
                # Traitez ici le rejet de la commande
                order.status = 'REJECTED'  # Modification du statut de la commande
                order.save()
                return JsonResponse({'message': 'Order rejected'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @login_required
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def place_order(request):
        if request.method == 'POST':
            # Extract clothes IDs from the request data
            clothes_ids = request.data.get('clothes_ids', [])  # Assuming 'clothes_ids' is the key in the request data
            pickup_date = request.data.get('pickup_date')

            # Check if clothes_ids is not empty
            if not clothes_ids:
                return JsonResponse({'error': 'No clothes selected'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if pickup_date is provided
            if not pickup_date:
                return JsonResponse({'error': 'Pickup date is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new Cart for the current user
            current_user = request.user
            cart = Cart.objects.create(user=current_user)

            # Process each clothes ID and create CartItem
            for clothes_id in clothes_ids:
                try:
                    clothes = Clothes.objects.get(pk=clothes_id)
                except Clothes.DoesNotExist:
                    return JsonResponse({'error': f'Clothes with ID {clothes_id} not found'}, status=status.HTTP_404_NOT_FOUND)

                # Create CartItem instance
                cart_item = CartItem.objects.create(clothes=clothes, cart=cart)

            # Save the Cart and CartItems
            cart.save()
            cart_item.save()

            # Return a success response
            return JsonResponse({'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @login_required
    @api_view(['GET'])
    def track_order(request, order_id):
        try:
            order = Order.objects.get(pk=order_id, client=request.user)
            return render(request, 'cart.html', {'order': order})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def process_order(cls, request, order_id):
        try:
            order = Order.objects.get(pk=order_id, client=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if order.status != 'SALE':  # Assuming 'PENDING' is the initial status of an order
            return Response({'error': 'Order cannot be processed'}, status=status.HTTP_400_BAD_REQUEST)

        # Example logic for processing an order
        if order.is_accepted:
            return redirect('cart_view')  # Redirect to cart view if order is accepted
        else:
            return redirect('home')  # Redirect to login view if order is not accepted

    def delete_order(request):
        pass

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        # Personnalisation de la création d'un nouvel élément de panier
        serializer.save(user=self.request.user)  # Attribuer l'utilisateur actuel comme propriétaire de l'élément de panier

    def add_clothes(request):
        pass

    def delete_clothes(request):
        pass

# Define the cart_summary view
@login_required
def cart_summary(request):
    # Retrieve the current user's cart
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []

    return render(request, 'cart/cart_summary.html', {'cart_items': cart_items})
"""

from django.http import JsonResponse, HttpResponseBadRequest


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        clothes_id = int(request.POST.get('clothes_id'))
        clothes_qty = int(request.POST.get('clothes_qty'))

        # Lookup for the item in the DB
        clothes = get_object_or_404(Clothes, id=clothes_id)

        # Ajouter l'article au panier avec mise à jour de la quantité
        cart.add(clothes=clothes, quantity=clothes_qty)

        # Vérification que l'article a bien été ajouté
        cart_quantity = cart.__len__()
        return JsonResponse({'qty': cart_quantity})
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff
        clothes_id = int(request.POST.get('clothes_id'))

        cart.delete(clothes=clothes_id)
    
        return redirect('cart_summary')


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff
        clothes_id = int(request.POST.get('clothes_id'))
        clothes_qty = int(request.POST.get('clothes_qty'))

        cart.update(clothes=clothes_id, quantity=clothes_qty)

        response = JsonResponse({'qty':clothes_qty})
        return response

def cart_summary(request):
    cart = Cart(request)
    cart_clothes = cart.get_cloths()
    quantities = cart.get_quants()  
    totals = cart.cart_total()
    return render(request, "cart/cart_summary.html", {"cart_clothes": cart_clothes, "quantities": quantities, "totals": totals})