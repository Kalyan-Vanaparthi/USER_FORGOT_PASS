from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.TextField()
    pic     = models.ImageField()