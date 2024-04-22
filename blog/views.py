import random
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from authentication.models import MyUser
from blog.models import Post, FollowUser, LikePost, Comment
from django.contrib import messages, auth


@login_required(login_url='/auth/login')
def home_view(request):
    posts = Post.objects.filter(is_published=True)
    users = MyUser.objects.all()[:4]
    profile = MyUser.objects.filter(user=request.user).first()
    comments = Comment.objects.all()
    for post in posts:
        post.comments = list(filter(lambda x: x.post.id == post.id, comments))

    if request.method == "POST":
        data = request.POST
        obj = Comment.objects.create(author=profile, message=data['message'], post_id=data['post_id'])
        obj.save()
        return redirect(f"/#{data['post_id']}")

    # user_following = FollowUser.objects.filter(follower=request.user.username)

    # all_users = User.objects.all()
    # user_following_all = []
    #
    # for user in user_following:
    #     user_list = User.objects.get(username=user.user)
    #     user_following_all.append(user_list)
    #
    #     new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    #     current_user = User.objects.filter(username=request.user.username)
    #     final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    #     random.shuffle(final_suggestions_list)
    #
    #     username_profile = []
    #     username_profile_list = []
    #
    #     for users in final_suggestions_list:
    #         username_profile.append(users.id)
    #
    #     for ids in username_profile:
    #         profile_list = MyUser.objects.filter(id_user=ids)
    #         username_profile_list.append(profile_list)
    #
    #     suggestions_username_profile_list = list(chain(*username_profile_list))

    d = {
        'posts': posts,
        'users': users,
        'profile': profile,
    }

    return render(request, 'index.html', context=d)


@login_required(login_url='/auth/login')
def upload_view(request):
    if request.method == 'POST':
        profile = MyUser.objects.filter(user=request.user).first()
        # profile = request.user.username
        image = request.FILES.get('image_upload')
        obj = Post.objects.create(author=profile, image=image)
        obj.save()
        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='/auth/login')
def follow(request):
    profile_id = request.GET.get('following_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    profile = MyUser.objects.filter(id=profile_id).first()
    follow_exists = FollowUser.objects.filter(follower=my_user, following_id=profile_id)

    if not follow_exists.exists():
        obj = FollowUser.objects.create(follower=my_user, following_id=profile_id)
        obj.save()
        profile.follower_count += 1
        profile.save(update_fields=['follower_count'])

    else:
        follow_exists.delete()
        profile.follower_count -= 1
        profile.save(update_fields=['follower_count'])
    return redirect('/')


@login_required(login_url='/auth/login')
def like(request):
    post_id = request.GET.get('post_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    my_post = Post.objects.filter(id=post_id).first()
    like_exists = LikePost.objects.filter(author=my_user, post_id=post_id)

    if not like_exists.exists():
        obj = LikePost.objects.create(author=my_user, post_id=post_id)
        obj.save()
        my_post.like_count += 1
        my_post.save(update_fields=['like_count'])

    else:
        like_exists.delete()
        my_post.like_count -= 1
        my_post.save(update_fields=['like_count'])
    return redirect('/')


def sighup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = MyUser.objects.create(user=user_model, id_user=user_model.id)
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
            image = user_profile.profile_picture
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_picture = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_picture = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('/setting')

    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='/auth/login')
def profile_view(request, pk):
    # user_object = User.objects.get(id=pk)
    # profile_id = request.GET.get('following_id')
    # profile = MyUser.objects.filter(id=profile_id).first()

    # user_profile = MyUser.objects.get(id=user_object)
    user_posts = Post.objects.filter(id=pk)
    length_posts = len(user_posts)

    follower = request.user.username
    following = pk

    # if FollowUser.objects.filter(follower=follower, following=following).first():
    # button_text = 'Unfollow'

    # else:
    #     button_text = 'Follow'
    user_followers = len(FollowUser.objects.filter(following=pk))
    user_following = len(FollowUser.objects.filter(follower=pk))
    context = {
        # 'user_object': user_object,
        # 'user_profile': user_profile,
        'user_posts': user_posts,
        'length_posts': length_posts,
        # 'button_text': button_text,

        'user_followers': user_followers,
        'user_following': user_following,
    }


    return render(request, 'profile.html', context)


@login_required(login_url='/auth/login')
def search_view(request):
    return render(request, 'search.html')
