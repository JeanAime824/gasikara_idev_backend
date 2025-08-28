from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Le nom d\'utilisateur doit être configuré.'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, password, **extra_fields)
    

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrateur'),
        ('responsable', 'Responsable'),
    )

    email = None
    user_type = models.CharField(max_length=25, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.user_type == 'admin'
    
    @property
    def is_responsable(self):
        return self.user_type == 'responsable'