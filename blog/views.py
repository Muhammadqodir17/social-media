import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from authentication.models import MyUser
from blog.models import Post, FollowUser, LikePost, Comment
from django.contrib import messages, auth


@login_required(login_url='/auth/login')
def home_view(request):
    user = MyUser.objects.filter(user=request.user).first()
    my_followers = FollowUser.objects.filter(follower=user).values_list('following', flat=True)
    posts = Post.objects.filter(is_published=True, author__in=my_followers)

    that_followers = MyUser.objects.filter(id__in=my_followers)
    followers_following = FollowUser.objects.filter(follower__in=that_followers).values_list('following', flat=True)
    followings_profile = MyUser.objects.filter(id__in=followers_following)
    random_list_followings_profile = list(followings_profile.all())
    random.shuffle(random_list_followings_profile)

    followed_user_ids = FollowUser.objects.filter(follower=user).values_list('following__user__id', flat=True)

    profile = MyUser.objects.filter(user=request.user).first()
    comments = Comment.objects.all()
    for post in posts:
        post.comments = list(filter(lambda x: x.post.id == post.id, comments))

    if request.method == "POST":
        data = request.POST
        obj = Comment.objects.create(author=profile, message=data['message'], post_id=data['post_id'])
        obj.save()
        return redirect(f"/#{data['post_id']}")

    d = {
        'posts': posts,
        'user': user,
        'users': random_list_followings_profile[:5],
        'profile': profile,
        'followed_user_ids': followed_user_ids
    }

    return render(request, 'index.html', context=d)


@login_required(login_url='/auth/login')
def upload_view(request):
    if request.method == 'POST':
        profile = MyUser.objects.filter(user=request.user).first()
        image = request.FILES.get('image_upload')
        obj = Post.objects.create(author=profile, image=image)
        obj.save()
        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='/auth/login')
def follow(request):
    random_following = request.GET.get('following_id')
    follower = MyUser.objects.filter(user__username=request.POST.get('follower')).first()
    following = MyUser.objects.filter(user__username=request.POST.get('following')).first()
    if random_following:
        follower = MyUser.objects.filter(user__username=request.user).first()
        following = MyUser.objects.filter(user__id=random_following).first()

    follow_exists = FollowUser.objects.filter(follower=follower, following=following)

    if not follow_exists:
        obj = FollowUser.objects.create(follower=follower, following=following)
        obj.save()
        follower.following_count += 1
        following.follower_count += 1
        follower.save(update_fields=['following_count'])
        following.save(update_fields=['follower_count'])

    else:
        follower.following_count -= 1
        following.follower_count -= 1
        follower.save(update_fields=['following_count'])
        following.save(update_fields=['follower_count'])
        follow_exists.delete()
    if random_following:
        return redirect('/')
    return redirect(f'/profile/{following.user.id}')


@login_required(login_url='/auth/login')
def like(request):
    post_id = request.GET.get('post_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    my_post = Post.objects.filter(id=post_id).first()
    like_exists = LikePost.objects.filter(author=my_user, post_id=post_id)

    if my_post.author == my_user:
        return redirect(f'/#{post_id}')

    if not like_exists.exists():
        obj = LikePost.objects.create(author=my_user, post_id=post_id)
        obj.save()
        my_post.like_count += 1
        my_post.save(update_fields=['like_count'])

    else:
        like_exists.delete()
        my_post.like_count -= 1
        my_post.save(update_fields=['like_count'])
    return redirect(f'/#{post_id}')


def sighup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            # if User.objects.filter(email=email).exists():
            #     messages.info(request, 'Email already Taken')
            #     return redirect('/signup')
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already Taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = MyUser.objects.create(user=user_model)
                new_profile.save()
                return redirect('/setting')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('/signup')
    return render(request, 'signup.html')


@login_required(login_url='/auth/login')
def settings_view(request):
    user_profile = MyUser.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            name = request.POST['name']
            user_profile.user.first_name = name
            user_profile.user.username = request.POST['username']
            user_profile.bio = request.POST['bio']
            user_profile.save()
            user_profile.user.save()

        if request.FILES.get('image') is not None:
            name = request.POST['name']
            user_profile.profile_picture = request.FILES.get('image')
            user_profile.user.first_name = name
            user_profile.user.username = request.POST['username']
            user_profile.bio = request.POST['bio']
            user_profile.save()
            user_profile.user.save()

        return redirect('/setting')

    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='/auth/login')
def profile_view(request, pk):
    user = MyUser.objects.filter(user__id=pk).first()
    follower = MyUser.objects.get(user=request.user)

    user_posts = Post.objects.filter(author__user__id=pk)
    length_posts = len(user_posts)

    if FollowUser.objects.filter(follower=follower, following=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_follower = len(FollowUser.objects.filter(following=user))
    following_user = len(FollowUser.objects.filter(follower=user))

    context = {
        'user_posts': user_posts,
        'user': user,
        'follower': follower,
        'length_posts': length_posts,
        'button_text': button_text,
        'user_follower': user_follower,
        'following_user': following_user,
    }

    return render(request, 'profile.html', context)


@login_required(login_url='/auth/login')
def search_view(request):
    search = request.GET.get('search')
    if search:
        user = MyUser.objects.filter(user__username__icontains=search)
        print(user)
    else:
        user = MyUser.objects.all()

    context = {
        'user': user,
        'search': search
    }

    return render(request, 'search.html', context)


@login_required(login_url='/auth/login')
def delete_post_view(request, pk):
    del_post = Post.objects.filter(id=pk).first()
    del_user = request.user

    if del_post.author.user != del_user:
        return redirect('/')
    del_post.delete()
    return redirect('/')
