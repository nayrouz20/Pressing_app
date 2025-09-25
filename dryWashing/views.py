from django.shortcuts import render, redirect
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_jwt.settings import api_settings
from django.conf import settings
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from .models import Clothes
from cart.models import CartItem, Cart, Order
from .serializers import ClothesSerializer
from rest_framework.decorators import api_view
from .models import BlacklistedToken
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.

class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            # Redirection après la connexion réussie
            response = Response({'token': token}, status=status.HTTP_200_OK)
            response['Location'] = settings.LOGIN_REDIRECT_URL
            messages.success(request,("vous avez été connecté avec succès"))
            return response

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        token = request.auth
        if token:
            BlacklistedToken.objects.create(token=token)
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
      # Exemple de vue nécessitant une authentification pour accéder
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def home(request):
        clothes = Clothes.objects.all()
        latest_order = None
        if request.user.is_authenticated:
            latest_order = Order.objects.filter(client=request.user).order_by('-id').first()
        return render(request, 'pressing/home.html', {
            'clothes': clothes,
            'latest_order': latest_order,
        })
    
    @api_view(['GET'])
    def my_view(request):
        response = HttpResponse(content_type="text/html; charset=utf-8")
        # Votre logique de vue ici
        #return Response({'message': 'This is a protected view'}, status=status.HTTP_200_OK)
        return response
        
    # Exemple de vue nécessitant un administrateur pour accéder
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def admin_view(self, request):
        # Votre logique de vue ici
        return Response({'message': 'This is an admin-only view'}, status=status.HTTP_200_OK)

    def search(request):
        #determine si on a remplie le form
        if request.method == "POST":
            searched = request.POST['searched']
            #query the products DB model
            searched = Clothes.objects.filter(name__icontains=searched)
            
            if not searched:
                messages.success(request, "Désolé on ne nettoie pas ce linge")
                return render(request,'pressing/search.html',{})
            else:
                return render(request,'pressing/search.html',{'searched':searched})
        else:
            return render(request,'pressing/search.html',{})
    
class ClothesViewSet(viewsets.ModelViewSet):
        queryset = Clothes.objects.all()
        serializer_class = ClothesSerializer
