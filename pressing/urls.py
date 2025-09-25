"""
URL configuration for pressing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from register import views as v
from cart import views as vi
from payment import views as vip
from dryWashing.views import (
    UserViewSet, ClothesViewSet
)
# from cart.views import ( CartItemViewSet, CartViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path("register/",v.register,name="register"),
    path('login/', v.login_view, name="login"),
    path('logout/', v.logout_view, name="logout"),
    path('update_user/',v.update_user,name="update_user"),
    path('update_password/',v.update_password,name="update_password"),
    path('update_info/',v.update_info,name="update_info"),
    path('', include(router.urls)),
    # Chemins pour les vues utilisateur
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='logout'),
    path('my_view/', UserViewSet.my_view, name='my_view'),
    path('admin_view/', UserViewSet.admin_view, name='admin_view'),
    path('', include("django.contrib.auth.urls")),
    path('admin/',admin.site.urls),

    # Chemins pour les vues liées aux articles et au panier
    path('home/', UserViewSet.home, name='home'),
        path('search/', UserViewSet.search, name='search'),
    path('clothes/', ClothesViewSet.as_view({'get': 'list'}), name='clothes_list'),
    # path('cart/', CartViewSet.as_view({'get': 'cart'}), name='cart'),
    # path('process_order/<int:order_id>/', CartViewSet.process_order, name='process_order'),
    # path('track_order/<int:order_id>/', CartViewSet.track_order, name='track_order'),
    # Chemin pour la validation de commande par l'administrateur
    # path('validate_order/<int:order_id>/', CartViewSet.validate_order, name='validate_order'), 
    path('cart/', include('cart.urls')),
    path('cart_summary/', vi.cart_summary, name="cart_summary"),

    # payment paths
    path('payment/', include('payment.urls')),
    path('payment_success/', vip.payment_success, name="payment_success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
