from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=30)
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    alcohol = models.BooleanField(default=False, null=True)    
    talk = models.BooleanField(default=False, null=True)    
    smoke = models.BooleanField(default=False, null=True)    
    speed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default = 3, null=True)   
    gender = models.BooleanField(default=False, null=True) # False가 남자    
    manner = models.FloatField(default=36.5, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

