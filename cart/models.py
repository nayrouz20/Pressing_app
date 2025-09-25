from django.db import models
from dryWashing.models import Clothes, User
from django.utils import timezone

# Create your models here.
class CartItem(models.Model):
    Clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deposit_date = models.DateTimeField(default=timezone.now)
    pickup_date = models.DateTimeField(default=timezone.now)

    is_processed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.Clothes} - {self.deposit_date}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_checked_out = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart for {self.user.username}"

class Order(models.Model):
    STATUS = [
        ('SALE', 'Linge sale'),
        ('EN COURS DE TRAITEMENT', 'linge en cours de traitement'),
        ('PROPRE', 'Linge propre'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_orders"  # Ajoutez un related_name unique
    )
    status = models.CharField(max_length=22, choices=STATUS)
    # Ajoutez d'autres champs selon vos besoins (date de commande, articles commandés, etc.)

    def __str__(self):
        return f"Order {self.pk} - {self.status}"