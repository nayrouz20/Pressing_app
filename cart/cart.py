from dryWashing.models import Clothes, Profile
import json


class Cart:
    def __init__(self, request):
        self.session = request.session
        # get request 
        self.request = request
        # get the current session key if it exists
        cart = self.session.get('session_key')
        
        if cart is None:
            cart = self.session['session_key'] = {}
        
        self.cart = cart

    def db_add(self, clothes, quantity):  
        clothes_id = str(clothes)
        quantity = int(quantity)  # Assurez-vous que la quantité est bien un entier
        
        # Si l'article est déjà dans le panier
        if clothes_id in self.cart:
            # Ajout de la quantité sélectionnée à la quantité existante
            self.cart[clothes_id] += quantity
        else:
            # Sinon, on ajoute l'article avec la quantité sélectionnée
            self.cart[clothes_id] = quantity

        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # get the current user profile 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convertir le dictionnaire en une chaîne JSON
            carty = json.dumps(self.cart)
            # Sauvegarder `carty` dans le modèle de profil
            current_user.update(old_cart=carty)


    def add(self, clothes, quantity):  
        clothes_id = str(clothes.id)
        quantity = int(quantity)  # Assurez-vous que la quantité est bien un entier
        
        # Si l'article est déjà dans le panier
        if clothes_id in self.cart:
            # Ajout de la quantité sélectionnée à la quantité existante
            self.cart[clothes_id] += quantity
        else:
            # Sinon, on ajoute l'article avec la quantité sélectionnée
            self.cart[clothes_id] = quantity

        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # get the current user profile 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convertir le dictionnaire en une chaîne JSON
            carty = json.dumps(self.cart)
            # Sauvegarder `carty` dans le modèle de profil
            current_user.update(old_cart=carty)

    def __len__(self):
        return len(self.cart)

    def get_cloths(self):
        clothes_ids = self.cart.keys()
        # Utiliser les identifiants pour rechercher les vêtements dans la base de données
        clothes = Clothes.objects.filter(id__in=clothes_ids)
        return clothes

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, clothes, quantity):
        clothes_id = str(clothes)
        clothes_qty = int(quantity)

        #get car
        ourcart = self.cart
        # update dictionnary/cart
        ourcart[clothes_id] = clothes_qty

        self.session.modified = True
            # deal with logged in user
        if self.request.user.is_authenticated:
            # get the current user profile 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convertir le dictionnaire en une chaîne JSON
            carty = json.dumps(self.cart)
            # Sauvegarder `carty` dans le modèle de profil
            current_user.update(old_cart=carty)


        thing = self.cart
        return thing
    
    def delete(self, clothes):
        clothes_id = str(clothes)
        #delete from dictionnary/cart
        if clothes_id in self.cart:
            del self.cart[clothes_id]

        self.session.modified = True
        
                # deal with logged in user
        if self.request.user.is_authenticated:
            # get the current user profile 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convertir le dictionnaire en une chaîne JSON
            carty = json.dumps(self.cart)
            # Sauvegarder `carty` dans le modèle de profil
            current_user.update(old_cart=carty)


        thing = self.cart
        return thing

    def cart_total(self):
        clothes_ids = self.cart.keys()
        # Utiliser les identifiants pour rechercher les vêtements dans la base de données
        clothes = Clothes.objects.filter(id__in=clothes_ids)
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for item in clothes:  # Renommer la variable de boucle pour éviter le conflit avec le nom de la classe
                if item.id == key:
                    total += (item.price * value)
        return total
