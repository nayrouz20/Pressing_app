from django.db import models
from dryWashing.models import User, Clothes
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class ShippingAdress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255, blank=True, null=True)
    shipping_address2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=255, blank=True, null=True)
    shipping_state = models.CharField(max_length=255, blank=True, null=True)
    shipping_codePostal = models.CharField(max_length=255, blank=True, null=True)

    # don't pluralize address
    class Meta:
        verbose_name_plural ="Shipping Adress"

    def __str__(self):
        return f'Shipping Adress - {str(self.id)}'


class Order(models.Model):
    STATUS_CHOICES = [
        ("LINGE_RECU", "Linge reçu"),
        ("EN_COURS", "En cours de nettoyage"),
        ("PRET_A_LIVRER", "Prêt à livrer"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='LINGE_RECU'  # Par défaut
    )
    user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            null=True,
            blank=True,
            related_name="payment_orders"  # Ajoutez un related_name unique
        )   
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    date_delivered = models.DateTimeField(blank=True, null=True)
    related_name="payment_orders"

    def __str__(self):
        return f"Commande {self.id} - {self.status}"

# auto add delivered date
@receiver(pre_save, sender=Order)
def set_delivered_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.delivered and not obj.delivered:
            instance.date_delivered = now

class Order_item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)  # Renommé de quantite à quantity
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Renommé de prix à price

    def __str__(self):
        return f'Order Item - {str(self.id)}'


# create a user profile by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
     if created:
          user_shipping = ShippingAdress(user=instance)
          user_shipping.save()

#automate the profile thing
post_save.connect(create_shipping, sender=User)
