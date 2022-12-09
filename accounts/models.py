from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# 이미지 업로드 경로
def image_upload_path(instance, filename):
    return f'account/{instance.id}/{filename}'

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(max_length=30, null=True, default='익명의 밥알')
    username = None
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alcohol = models.BooleanField(default=False)    
    talk = models.BooleanField(default=False)    
    smoke = models.BooleanField(default=False)    
    speed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default = 3)   
    gender = models.BooleanField(default=False) # False가 남자    
    manner = models.FloatField(default=36.5)
    profile_image = ProcessedImageField(
        upload_to=image_upload_path,
        blank=True,
        null=True,
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 80},
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# class UserProfileImage(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profileimage')