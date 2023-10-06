from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager



class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return self.email
