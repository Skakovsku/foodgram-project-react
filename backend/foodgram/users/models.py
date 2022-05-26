from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('admin', 'admin'),
        ('user', 'user'),
        ('user_auth', 'user_auth')
    )
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(unique=True, max_length=100)
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='user_auth')

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'user_auth'
    
    class Meta:
        ordering = ('-pk',)
