from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password, nickname,  **kwargs):
        if not email:
            raise ValueError(_('The Email must be set'))
        user = self.model(
            email=email,
            nickname=nickname,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, nickname, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
        )
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser