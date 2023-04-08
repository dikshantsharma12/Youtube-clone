from django.db import models

from profile_page.models import UserDetails, VideoDetails

# Create your models here.


class LikedVideos(models.Model):

    user_id = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name='my_user')
    saved_videos = models.ForeignKey(
        VideoDetails, on_delete=models.CASCADE, related_name='saved_videos')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created_at',)


class SavedVideos(models.Model):
    user_id = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name='liked_by_user')
    liked_videos = models.ForeignKey(
        VideoDetails, on_delete=models.CASCADE, related_name='liked_videos')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created_at',)


class UnsavedVideos(models.Model):
    user_id = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name='disliked_by_user')
    disliked_videos = models.ForeignKey(
        VideoDetails, on_delete=models.CASCADE, related_name='disliked_videos')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created_at',)


class Comments(models.Model):
    commenter = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name='commenter')
    video = models.ForeignKey(
        VideoDetails, on_delete=models.CASCADE, related_name='commenting_video')
    comment = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created_at',)
