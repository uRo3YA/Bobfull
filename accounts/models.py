from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class User(AbstractUser):
    alcohol = models.BooleanField(default=False)    
    talk = models.BooleanField(default=False)    
    smoke = models.BooleanField(default=False)    
    speed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default = 3)   
    gender = models.BooleanField(default=False) # False가 남자    
    manner = models.FloatField(default=36.5)    