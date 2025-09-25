from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib import messages
from dryWashing.models import User, Profile
from .forms import UserInfoForm
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import User, ShippingAdress
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # Import du nouveau formulaire

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()
            login(request, user)  # Connexion automatique après l'inscription
            return redirect("home")  # Redirection après l'inscription
    else:
        form = CustomUserCreationForm()

    return render(request, "register/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
               # do some shopping cart stuff
                current_user, created = Profile.objects.get_or_create(user=request.user)

                # get their saved cart from DB
                saved_cart = current_user.old_cart
                # convert DB string to python dict
                if saved_cart:
                    # convert to dict using json
                    converted_cart = json.loads(saved_cart)
                    # add the loaded cart dictionnary to our session
                    # get the cart 
                    cart = Cart(request)
                    #loop through the cart dict to our session
                    for key,value in converted_cart.items():
                        cart.db_add(clothes=key, quantity=value)



                return redirect('home')  # Redirection après connexion réussie
            else:
                return render(request, "registration/login.html", {"form": form, "error": "Invalid username or password."})
        else:
            return render(request, "registration/login.html", {"form": form, "error": "Invalid form data."})
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')
    
from .forms import CustomUserChangeForm, ChangePasswordForm
from django.contrib.auth.models import User
def update_user(request):
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour modifier votre profil.")
        return redirect('login')

    current_user = request.user
    user_form = CustomUserChangeForm(request.POST or None, instance=current_user)
    password_form = ChangePasswordForm(current_user, request.POST or None)

    if request.method == "POST":
        if "update_info" in request.POST:  # Mise à jour des informations utilisateur
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Vos informations ont été mises à jour avec succès.")
                return redirect('update_user')

        elif "update_password" in request.POST:  # Mise à jour du mot de passe
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, current_user)  # Évite la déconnexion
                messages.success(request, "Votre mot de passe a été changé avec succès.")
                return redirect('update_user')
            else:
                for error in list(password_form.errors.values()):
                    messages.error(request, error)

    return render(request, "update/update_user.html", {
        'user_form': user_form,
        'password_form': password_form
    })
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #did they fill out the form
        if request.method == 'POST': 
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "votre mot de passe a été changé avec succés")
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')  
                  
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update/update_password.html", {'form':form})     
    else:
        messages.error(request, "Vous devez être connecté pour mettre à jour votre mot de passe.")
        return redirect('login')
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)

        try:
            # Get current user's shipping info
            shipping_user = ShippingAdress.objects.get(user=request.user)  # Assuming user is a ForeignKey in ShippingAdress
        except ShippingAdress.DoesNotExist:
            # If no shipping address exists, create a new one
            shipping_user = ShippingAdress(user=request.user)
            shipping_user.save()

        # Get the original user form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get the user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if request.method == "POST":
            if form.is_valid() and shipping_form.is_valid():  # Both forms must be valid
                form.save()
                shipping_form.save()

                # Stocker les données validées du formulaire dans la session
                request.session['shipping_info'] = shipping_form.cleaned_data

                messages.success(request, "Vos informations ont été mises à jour avec succès.")
                return redirect('home')
            else:
                messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

        return render(request, "update/update_info.html", {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, "Vous devez être connecté pour mettre à jour votre profil.")
        return redirect('login')