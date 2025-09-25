from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Clothes, Profile
from cart.models import CartItem, Cart, Order
# from django.contrib.auth.models import User
# Register your models here.


admin.site.register(Clothes)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Profile)

User = get_user_model()
#mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile
#extend user model 
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]    

#unregister the old way
admin.site.unregister(User)

#re-register the new way
admin.site.register(User, UserAdmin)
