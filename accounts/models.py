from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractUser):
    username = models.CharField(max_length=30)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    alcohol = models.BooleanField(default=False, null=True)    
    talk = models.BooleanField(default=False, null=True)    
    smoke = models.BooleanField(default=False, null=True)    
    speed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default = 3, null=True)   
    gender = models.BooleanField(default=False, null=True) # False가 남자    
    manner = models.FloatField(default=36.5, null=True)


