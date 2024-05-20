from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=13, unique=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    is_agent = models.BooleanField(default=False)
    # Profile bilan bog'lanish
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    last_update = models.DateField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} User"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField()
    is_agent = models.BooleanField(default=False)
    telegram_username = models.CharField(max_length=100)
    x_link = models.URLField(null=True, blank=False)
    m_link = models.URLField(null=True, blank=False)
    l_link = models.URLField(null=True, blank=False)
    profile_image = models.ImageField(upload_to='profile_images/', default="default_profile.jpg",
                                      blank=True, null=True)
    last_update = models.DateField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'
