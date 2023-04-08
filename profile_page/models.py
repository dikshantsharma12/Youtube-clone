from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

user = get_user_model()


def get_curr_video_id():
    video_id_list = VideoDetails.objects.values_list("video_id", flat=True)

    if len(video_id_list) == 0:
        return 1
    curr_video_id = video_id_list[len(video_id_list)-1]+1
    return curr_video_id


def user_directory_path(instance, filename):
    return "profile/images/"+'user_{0}/{1}'.format(instance.user_id, filename)


def user_video_directory(instance, filename):

    return "profile/videos/" + 'user_{0}/video_{1}/{2}'.format(instance.user_id, get_curr_video_id(), filename)


def user_thumbnail_directory(instance, filename):

    return "profile/videos/" + 'user_{0}/video_{1}/thumbnail/{2}'.format(instance.user_id, get_curr_video_id(), filename)


class UserDetails(models.Model):
    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(
        blank=True, upload_to=user_directory_path, default="user-icon.png")
    gender = models.CharField(max_length=30, blank=True)
    dob = models.DateField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField(
        'self', related_name='following', symmetrical=False)

    def __str__(self):
        return str(self.user_id)


class VideoDetails(models.Model):
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    video_id = models.AutoField(primary_key=True)
    video = models.FileField(
        upload_to=user_video_directory,
        validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    video_title = models.TextField(blank=False, null=False)
    video_description = models.TextField(blank=True)
    video_category = models.CharField(max_length=50)
    video_views = models.BigIntegerField(default=0)
    video_likes = models.BigIntegerField(default=0)
    video_dislikes = models.BigIntegerField(default=0)
    video_comments = models.BigIntegerField(default=0)
    video_thumbnail = models.ImageField(
        upload_to=user_thumbnail_directory, default="thumbnail.png")

    def __str__(self):
        return str(self.video_id)


class Follow(models.Model):
    follower = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name='myfollowing')
    followee = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name='myfollowers')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created_at',)


class History(models.Model):
    user_id = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name='history_user')
    video_id = models.ForeignKey(
        VideoDetails, on_delete=models.CASCADE, related_name='history_videos')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created_at',)
