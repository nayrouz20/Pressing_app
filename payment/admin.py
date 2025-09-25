from django.contrib import admin
from .models import ShippingAdress, Order, Order_item
from django.contrib.auth.models import User

# register the model on the admin section thing
admin.site.register(ShippingAdress)
admin.site.register(Order)
admin.site.register(Order_item)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_at')  # Afficher les commandes avec leur statut
    list_filter = ('status',)  # Filtrer par statut
    search_fields = ('customer__username', 'id')  # Recherche par client ou ID de commande

# create an order item inline 
class OrderItemInline(admin.StackedInline):
    model = Order_item
    extra = 0

# extend our Order Model 
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "delivered", "date_delivered"]
    inlines = [OrderItemInline]

# unregister order model 
admin.site.unregister(Order)

# re-register our order and OrderAdmin
admin.site.register(Order, OrderAdmin)
