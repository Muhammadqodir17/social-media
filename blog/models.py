from datetime import datetime

from django.db import models

from authentication.models import MyUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    objects = None
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')
    like_count = models.PositiveIntegerField(default=0, blank=True)

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.author.user.username}"


class Comment(models.Model):
    objects = None
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    message = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} : {self.author.user.username}"


class LikePost(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.user.username} | {self.post.author.user.username}"


class FollowUser(models.Model):
    follower = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='follower', blank=True)
    following = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='following', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.user.username} | {self.following.user.username}"




