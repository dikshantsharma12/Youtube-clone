from django.contrib import admin
from .models import LikedVideos,SavedVideos,UnsavedVideos,Comments
# Register your models here.
admin.site.register(LikedVideos)
admin.site.register(SavedVideos)
admin.site.register(UnsavedVideos)
admin.site.register(Comments)