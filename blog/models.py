from django.db import models

from authentication.models import MyUser


class Post(models.Model):
    objects = None
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    objects = None
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


class FollowUser(models.Model):
    objects = None
    follower = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='following')

    created_at = models.DateTimeField(auto_now_add=True)



