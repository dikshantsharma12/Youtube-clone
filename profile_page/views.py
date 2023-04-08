from django.shortcuts import render, redirect
from profile_page.models import UserDetails, VideoDetails, Follow
from django.contrib.auth.models import User
import json
from django.http import JsonResponse

# Create your views here.


def profile(request,profile_id):
    if request.method == "POST":
        if "firstname" in request.POST:
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            profile_image = request.FILES.get('profile_image')
            gender = request.POST['gender']
            dob = request.POST['dob']
            location = request.POST['location']
            user_profile = UserDetails.objects.get(user_id=request.user.id)
            main_user = User.objects.get(id=request.user.id)
            if first_name:
                user_profile.first_name = first_name
                main_user.first_name = first_name
            if last_name:
                user_profile.last_name = last_name
                main_user.last_name = last_name
            if gender:
                user_profile.gender = gender
            if dob:
                user_profile.dob = dob
            if location:
                user_profile.location = location
            if profile_image:
                user_profile.image = profile_image

            user_profile.save()
            main_user.save()
        else:
            id = request.user.id
            video_details = VideoDetails.objects.create(
                user_id=UserDetails.objects.get(user_id=id),
                video=request.FILES.get("uploaded_video"),
                video_title=request.POST["title"],
                video_description=request.POST['description'],
                video_category=request.POST["video_category"],
                video_thumbnail=request.FILES.get("video_thumbnail")
            )
            video_details.save()
        return redirect("/profile")
    else:
        obj = UserDetails.objects.get(user_id=request.user.id)
        youtuber = UserDetails.objects.get(user_id = profile_id)
        profile_videos = VideoDetails.objects.filter(user_id = profile_id).order_by('-video_id')
        home_videos = VideoDetails.objects.filter(user_id = profile_id).order_by('-video_views')[:5]
        
        ## Subscriptions
        subscribed_people = Follow.objects.filter(followee_id = request.user.id).values('follower_id')
        subscribed_people_list = [youtuber['follower_id'] for youtuber in subscribed_people]
        subscribed_people = UserDetails.objects.filter(user_id__in = subscribed_people_list)

        is_followed = False
        try:
            is_followed = Follow.objects.get(followee = request.user.id , follower = profile_id)
        except:
            print("User Not Found")
        try:
            total_followers = len(Follow.objects.filter(follower = profile_id))
            print(total_followers)
            
        except: 
            print("No Followers")

        context = {
            'user_details': obj,
            'youtuber':youtuber,
            'home_videos': home_videos,
            'profile_videos':profile_videos,
            'already_followed':is_followed,
            'total_subscribers': total_followers,
            'subscriptions':subscribed_people
        }
        return render(request, 'profile.html', context)

def subscribe(request):

    curr_user = request.user.id
    print(request.body)
    request_data = json.loads(request.body)
    to_follow =int(request_data['youtuber'])
    option = request_data['option']

    print(option)
    
    if option == "subscribe":
        follow =   Follow.objects.create(
                follower = UserDetails.objects.get(user_id = to_follow),
                followee = UserDetails.objects.get(user_id = curr_user)
            )
        follow.save()

        return JsonResponse({
            'status':"subscribed"
        })
    else:
        unfollow = Follow.objects.get(
                follower = UserDetails.objects.get(user_id = to_follow),
                followee = UserDetails.objects.get(user_id = curr_user)
        ) 
        unfollow.delete()
        return JsonResponse({
            'status':"unsubscribed"
        })