from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 헬퍼 클래스
class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, email, password, nickname, name, **kwargs):
        if not email:
            raise ValueError('must have user email')
        user = self.model(
            email = email,
            nickname = nickname,
            name = name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            email = email,
            password = password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.alcohol = False
        superuser.talk = False
        superuser.smoke = False
        superuser.speed = 3
        superuser.gender = False
        superuser.manner = 36.5

        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser

# AbstractBaseUser를 상속해서 유저 커스텀   
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    nickname = models.CharField(default="", max_length=100, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 추가정보
    alcohol = models.BooleanField(default=False, null=True)    
    talk = models.BooleanField(default=False, null=True)    
    smoke = models.BooleanField(default=False, null=True)    
    speed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default = 3, null=True)   
    gender = models.BooleanField(default=False, null=True) # False가 남자    
    manner = models.FloatField(default=36.5, null=True)  

    # User 모델의 필수 field
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)    
    is_superuser = models.BooleanField(default=False)

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 email로 설정
    USERNAME_FIELD = 'email'

    # 필수로 작성해야하는 field
    # REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.nickname


