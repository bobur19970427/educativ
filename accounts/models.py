from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def get_avatar(instance, filename):
    return "users/%s" % (filename)

class User(AbstractUser):

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    complete = models.IntegerField(default=0)
    is_teacher = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=get_avatar, default='users/default.png')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.username

