from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_save

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.token

class User(AbstractUser):
    # Ajoutez d'autres champs selon vos besoins
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set_custom',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set_custom',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name="custom_user",
    )

class Meta:
        pass  # Laisser la classe Meta vide

class Clothes(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/clothes/')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'clothes'

User = get_user_model()

class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
        date_modified = models.DateTimeField(User, auto_now=True)
        phone = models.CharField(max_length=20, blank=True, null=True)
        address1 = models.CharField(max_length=200, blank=True, null=True)
        address2 = models.CharField(max_length=200, blank=True)
        city = models.CharField(max_length=200, blank=True, null=True)
        state = models.CharField(max_length=200, blank=True, null=True)
        codePostal = models.CharField(max_length=200, blank=True, null=True)
        old_cart = models.CharField(max_length=200, blank=True, null=True)

        def __str__(self):
            return f"Profil de {self.user.username}"
# create a user profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
     if created:
          user_profile = Profile(user=instance)
          user_profile.save()

#automate the profile thing
post_save.connect(create_profile, sender=User)
