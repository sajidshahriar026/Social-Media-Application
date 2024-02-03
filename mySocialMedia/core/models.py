from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.


User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profile_images", default="blank-profile-picture.png")
    location = models.CharField(max_length=100, blank=True)

    def get_username(self):
        return self.user.username

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="post_images", blank=True)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField()
    number_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.caption


class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' ' + str(self.post.id) + ' ' + str(self.user.id)

    def liked_by(self):
        return self.user.username

    def posted_by(self):
        return self.post.user.username


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return self.follower.username + ' ' + self.following.username

    def get_follower(self):
        return self.follower.username

    def get_following(self):
        return self.following.username