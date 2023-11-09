from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4

class UserManager(BaseUserManager):
    
    def create_user(self, username, email, first_name=None, last_name=None, password=None, is_admin=False, is_customer=False):
        if username is None:
            raise TypeError("User should have a username")
        if email is None:
            raise TypeError("User should have email")
        
        user = self.model(username=username, email=self.normalize_email(email), first_name=first_name, last_name=last_name, is_admin=is_admin, is_customer=is_customer)
        user.set_password(password)
        user.save()
        return user
    
    def create_admin(self, username, email, first_name, last_name, password=None, is_admin=False,  is_customer=False):
        user = self.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password, is_admin=is_admin, is_customer=is_customer)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user
    
    def create_customer(self, username, email, first_name, last_name, password=None, is_admin=False, is_customer=False):
        user = self.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password, is_admin=is_admin,  is_customer=is_customer)
        user.is_customer = True
        user.save()
        return user
    
    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }