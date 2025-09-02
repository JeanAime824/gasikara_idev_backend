from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role=None, **extra_fields):
        if not username:
            raise ValueError(_('The username field must be set'))
        if not email:
            raise ValueError(_('The email address field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)
    

class User (AbstractBaseUser, PermissionsMixin):
    ROLE = (
        ('ADMIN', 'Administrateur'),
        ('MANAGER','Responsable'),
    )
    uid=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    role=models.CharField(
        max_length=20,
        choices=ROLE, null=True, blank=True,
        default='MANAGER'
    )
    username=models.CharField(
        max_length=25,
        verbose_name=_('Username'),
        unique=True, db_index=True
    )
    email=models.EmailField(
        verbose_name=_('Email address'),
        unique=True, db_index=True
    )

    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name=_('User')
        verbose_name_plural=_('Users')

    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def is_manager(self):
        return self.role == 'MANAGER'
    