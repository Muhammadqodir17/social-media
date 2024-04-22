from django.contrib.auth.models import User
from django.db import models


class MyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pic/', default='btm-baner-avatar.png')
    id_user = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    followers = models.IntegerField(default=0, blank=True, null=True)
    follower_count = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return f'{self.user.username}'
3