from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    FOODY = 'foody'
    CHEF = 'chef'
    MASTER_CHEF = 'master_chef'
    ROLE_CHOICES = [
        (FOODY, 'Foody'),
        (CHEF, 'Chef'),
        (MASTER_CHEF, 'Master Chef'),
    ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=FOODY)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # You can also add other fields as needed
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
