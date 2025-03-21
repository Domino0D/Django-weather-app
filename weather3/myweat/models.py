from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class City(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='cities')
    city = models.CharField(max_length=25)

    def __str__(self):
        return self.city

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    Temp_scale = models.CharField(max_length=1, choices=[('C', 'Celsjusz'), ('F', 'Fahrenheit')], default='C')
    
    def __str__(self):
        return self.user.username


# Create your models here.
