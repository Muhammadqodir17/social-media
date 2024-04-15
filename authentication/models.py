from django.contrib.auth.models import User
from django.db import models


class MyUser(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pic/', blank=True, null=True)

    def __str__(self):
        return self.user.username
