from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("setting", views.setting, name="setting"),
    path("upload", views.upload, name="upload"),
    path("like-post/<int:post_id>", views.like_post, name="like-post"),
    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("search", views.search_user, name="search"),
    path("signin", views.signin, name="signin"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout, name="logout")
]