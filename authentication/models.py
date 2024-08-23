from django.contrib.auth.models import User
from django.db import models


class MyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pic/', default='btm-baner-avatar.png')
    bio = models.TextField(blank=True)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'
