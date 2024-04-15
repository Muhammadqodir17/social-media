from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from authentication.models import MyUser
from blog.models import Post, FollowUser, LikePost, Comment


@login_required(login_url='/auth/login')
def home_view(request):
    posts = Post.objects.filter(is_published=True)
    users = MyUser.objects.all()[:4]
    profile = MyUser.objects.filter(user=request.user).first()
    comments = Comment.objects.all()
    for post in posts:
        post.comments = list(filter(lambda x: x.post.id == post.id, comments))

    d = {
        'posts': posts,
        'users': users,
        'profile': profile,
    }

    if request.method == "POST":
        data = request.POST
        obj = Comment.objects.create(author=profile, message=data['message'], post_id=data['post_id'])
        obj.save()
        return redirect(f"/#{data['post_id']}")

    return render(request, 'index.html', context=d)


@login_required(login_url='/auth/login')
def follow(request):
    print('=' * 50)
    data = request.GET.get('following_id')
    print(data)
    print('=' * 50)
    follower = MyUser.objects.filter(user=request.user).first()
    following = MyUser.objects.filter(id=request.GET.get("following_id")).first()
    obj = FollowUser.objects.create(follower=follower, following=following)
    obj.save()
    return redirect('/')


@login_required(login_url='/auth/login')
def like(request):
    author = MyUser.objects.filter(user=request.user).first()
    post_id = request.GET.get('post_id')
    obj = LikePost.objects.create(author=author, post_id=post_id)
    obj.save()
    return redirect(f"/#{post_id}")


