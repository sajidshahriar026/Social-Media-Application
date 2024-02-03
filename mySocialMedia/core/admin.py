from django.contrib import admin

from .models import Profile, Post, LikePost, Follower


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "caption", "created_at", "number_of_likes"]


class LikePostAdmin(admin.ModelAdmin):
    list_display = ["id", "liked_by", "post", "posted_by"]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "get_username"]



class FollowerAdmin(admin.ModelAdmin):
    list_display = ["id", "get_follower", "get_following"]




admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(Follower, FollowerAdmin)


