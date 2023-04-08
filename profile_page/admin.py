from django.contrib import admin

# Register your models here.

from .models import UserDetails , VideoDetails, Follow, History 

admin.site.register(UserDetails)
admin.site.register(VideoDetails)
admin.site.register(Follow)
admin.site.register(History)