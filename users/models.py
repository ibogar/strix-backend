from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

username_validator = RegexValidator(
    regex=r'^[a-z0-9_]+$',
    message='Only lowercase letters, numbers and underscores allowed.'
)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=30, unique=True, validators=[username_validator])
    bio = models.TextField(max_length=140, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    