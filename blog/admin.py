from django.contrib import admin
from .models import Post, Comment, LikePost, FollowUser

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(FollowUser)

