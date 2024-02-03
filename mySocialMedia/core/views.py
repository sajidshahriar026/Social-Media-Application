from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from .models import Profile, Post, LikePost, Follower


# Create your views here.

@login_required(
    login_url="core:signin"
)
def index(request):
    current_user_profile = Profile.objects.get(user=request.user)

    followings = Follower.objects.filter(follower=request.user)

    posts_details = list()

    user_profile_suggestion_list = list()

    #exclude the current user and the admin
    all_user_list = User.objects.all().exclude(Q(id=1) | Q(id=request.user.id))

    for following in followings:
        all_user_list = all_user_list.exclude(id=following.following.id)

        profile_id_of_the_following = Profile.objects.get(user=following.following).id
        posts_from_the_following = Post.objects.filter(user=following.following).order_by('-created_at')

        for post in posts_from_the_following:
            post_detail = (post.created_at, profile_id_of_the_following, post)
            posts_details.append(post_detail)


    for user in all_user_list:
        user_profile = Profile.objects.get(user=user)
        user_profile_suggestion_list.append(user_profile)

    posts_details.sort(reverse=True)

    context = {
        "current_user_profile": current_user_profile,
        "posts_details": posts_details,
        "user_profile_suggestion_list": user_profile_suggestion_list
    }

    return render(request, "core/index.html", context)


@login_required(
    login_url="core:signin"
)
def profile(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    profile_user = User.objects.get(pk=profile.user.id)
    posts_by_the_profile_user = Post.objects.filter(user=profile_user).order_by('-created_at')
    number_of_posts = posts_by_the_profile_user.count()
    number_of_followers = Follower.objects.filter(following=profile_user).count()
    number_of_followings = Follower.objects.filter(follower=profile_user).count()

    is_following = True if Follower.objects.filter(follower=request.user, following=profile_user).exists() else False

    context = {
        "profile": profile,
        "profile_user": profile_user,
        "posts_by_the_profile_user": posts_by_the_profile_user,
        "number_of_posts": number_of_posts,
        "is_following": is_following,
        "number_of_followers": number_of_followers,
        "number_of_followings": number_of_followings
    }

    return render(request, "core/profile.html", context)

@login_required(
    login_url="core:signin"
)
def setting(request):
    user_profile = Profile.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":

        if request.FILES.get('profile_picture'):
            profile_picture = request.FILES.get('profile_picture')
        else:
            profile_picture = user_profile.profile_image

        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profile_image = profile_picture
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        redirect('core:setting')

    context = {
        "user_profile": user_profile
    }

    return render(request, "core/setting.html", context)

@login_required(
    login_url="core:signin"
)
def upload(request):
    if request.method == "POST":
        current_user = request.user
        if request.FILES.get('image_upload'):
            uploaded_image = request.FILES.get('image_upload')

            caption = request.POST['caption']

            new_post = Post.objects.create(
                user=current_user,
                image=uploaded_image,
                caption=caption,
                created_at=timezone.now()
            )
            new_post.save()
        else:
            messages.info(request, "Post can't be created without an image!!!")
            redirect('core:index')

    return redirect('core:index')



@login_required(
    login_url="core:signin"
)
def like_post(request, post_id):
    liking_user = request.user
    post = Post.objects.get(pk=post_id)

    #if user has already liked then it is an unlike action
    if LikePost.objects.filter(post=post, user=liking_user).exists():
        liked_post = LikePost.objects.get(post=post, user=liking_user)
        liked_post.delete()

        post.number_of_likes -= 1
        post.save()

        return redirect('core:index')
    #else the post is to be liked
    else:
        post_to_be_liked = LikePost.objects.create(post=post, user=liking_user)
        post_to_be_liked.save()

        post.number_of_likes += 1
        post.save()

        return redirect('core:index')



@login_required(
    login_url="core:signin"
)
def follow(request, profile_id):
    current_user = User.objects.get(pk=request.user.id)
    profile_to_be_followed = Profile.objects.get(pk=profile_id)
    user_to_be_followed = profile_to_be_followed.user
    print(user_to_be_followed)
    # A user can not follow oneself
    if current_user.id == user_to_be_followed.id:
        return redirect('core:profile', profile_id=profile_id)

    #if the user is already following the profile_user then it is an unfollow action
    elif Follower.objects.filter(follower=current_user, following=user_to_be_followed).exists():
        follow_relation_to_be_deleted = Follower.objects.filter(
            follower=current_user,
            following=user_to_be_followed
        )
        follow_relation_to_be_deleted.delete()
        return redirect('core:profile', profile_id=profile_id)
    # allow the user to follow
    else:
        new_follow = Follower.objects.create(
            follower=current_user,
            following=user_to_be_followed
        )
        new_follow.save()
        return redirect('core:profile', profile_id=profile_id)



@login_required(
    login_url="core:signin"
)
def search_user(request):

    profile_of_the_current_user = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        username_to_be_searched = request.POST['search_string']

        profiles_from_the_search = Profile.objects.filter(user__username__icontains=username_to_be_searched)

        context = {
            "profile_of_the_current_user": profile_of_the_current_user,
            "profiles_from_the_search": profiles_from_the_search
        }

        return render(request, 'core/search.html', context)
    else:
        return redirect('core:index')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("core:index")

        else:
            messages.info(request, "Invalid username and password")
            return redirect("core:signin")

    else:
        return render(request, "core/signin.html")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["password2"]

        if password != confirm_password:
            messages.info(request, "Password not matching")
            return redirect('core:signup')
        else:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('core:signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect('core:signup')
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password, )
                new_user.save()

                #first log the user in
                authenticated_new_user = auth.authenticate(username=username,password=password)
                auth.login(request, authenticated_new_user)

                # create profile for the user and redirect them to the setting page
                new_profile = Profile.objects.create(user=new_user)
                new_profile.save()

                return redirect('core:setting')


    else:
        return render(request, "core/signup.html")


@login_required(
    login_url="core:signin"
)
def logout(request):
    auth.logout(request)
    return redirect('core:signin')