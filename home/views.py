from django.shortcuts import render
from profile_page.models import UserDetails, VideoDetails,Follow,History
from video_page.models import SavedVideos,LikedVideos
from django.db import connection

# Create your views here.


def home(request):

    videos = VideoDetails.objects.all()
    custom = custom_sql()

    if request.user.is_authenticated:
        user_details = UserDetails.objects.get(user_id=request.user.id)
        subscribed_people = Follow.objects.filter(followee_id = request.user.id).values('follower_id')
        subscribed_people_list = [youtuber['follower_id'] for youtuber in subscribed_people]

        subscribed_people = UserDetails.objects.filter(user_id__in = subscribed_people_list)
        context = {
            'user_details': user_details,
            'videos': videos,
            'user_data': custom,
            'subscriptions':subscribed_people
        }
        return render(request, 'home.html', context)
    else:


        context = {
            'videos': videos,
            'user_data': custom,
        }
        return render(request, 'home.html', context)
def subscriptions(request):
    user_details = UserDetails.objects.get(user_id=request.user.id)
    user_id = request.user.id
    subscritions_list = Follow.objects.filter(followee_id = user_id).values('follower_id')
    subscritions_list = tuple(x['follower_id'] for x in subscritions_list)
    subscribed_people = Follow.objects.filter(followee_id = request.user.id).values('follower_id')
    subscribed_people_list = [youtuber['follower_id'] for youtuber in subscribed_people]

    subscribed_people = UserDetails.objects.filter(user_id__in = subscribed_people_list)
    
    params = {
        'l':subscritions_list
    }
    subscribed_videos = get_custom_subscriptions(params)
    
    context = {
        'subscribed_videos': subscribed_videos,
        'user_details':user_details,
        'subscriptions':subscribed_people
    }
    return render(request,'subscriptions.html', context)

def watch_later(request):
    user_details = UserDetails.objects.get(user_id=request.user.id)
    user_id= request.user.id
    saved_videos = LikedVideos.objects.filter(user_id = user_id).values('saved_videos')
    list_saved_videos = tuple(x['saved_videos'] for x in saved_videos)
    subscribed_people = Follow.objects.filter(followee_id = request.user.id).values('follower_id')
    subscribed_people_list = [youtuber['follower_id'] for youtuber in subscribed_people]

    subscribed_people = UserDetails.objects.filter(user_id__in = subscribed_people_list)

    params = {
        'l':list_saved_videos
    }
    saved_videos = get_custom_videos(params)
    context = {
        'saved_videos': saved_videos ,
        'user_details':user_details ,
        'subscriptions':subscribed_people
    }
    return render(request,'watch_later.html',context)

def liked_videos(request):
    user_details = UserDetails.objects.get(user_id=request.user.id)
    subscribed_people = Follow.objects.filter(followee_id = request.user.id).values('follower_id')
    subscribed_people_list = [youtuber['follower_id'] for youtuber in subscribed_people]

    subscribed_people = UserDetails.objects.filter(user_id__in = subscribed_people_list)

    user_id= request.user.id
    liked_videos = SavedVideos.objects.filter(user_id = user_id).values('liked_videos')
    list_liked_videos = tuple(x['liked_videos'] for x in liked_videos)
    params = {
        'l':list_liked_videos
    }
    liked_videos = get_custom_videos(params)
    context = {
        'liked_videos': liked_videos,
        'user_details':user_details,
        'subscriptions':subscribed_people
    }    
    return render(request,'liked_videos.html',context)

def history(request):
    user_details = UserDetails.objects.get(user_id=request.user.id)

    subscribed_people = Follow.objects.filter(followee_id = request.user.id).values('follower_id')
    subscribed_people_list = [youtuber['follower_id'] for youtuber in subscribed_people]
    subscribed_people = UserDetails.objects.filter(user_id__in = subscribed_people_list)
    
    user_id= request.user.id
    history_videos = History.objects.filter(user_id = user_id).values('video_id').order_by('created_at')
    list_history_videos = tuple(x['video_id'] for x in history_videos)
    params = {
        'l':list_history_videos
    }
    history_videos = get_history_videos(params)
    context = {
        'history_videos': history_videos,
        'user_details':user_details,
        'subscriptions':subscribed_people
    }    

    return render(request,'history.html',context)

def custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                            v.video_id, 
                            v.user_id_id, 
                            v.video_title,
                            u.first_name, 
                            u.last_name,
                            u.image,
                            v.video_views,
                            v.video_thumbnail
                        FROM 
                            public.profile_page_videodetails v
                        LEFT JOIN
                            public.profile_page_userdetails u
                        USING
                            (user_id_id)
                        ORDER BY
                            video_id desc
                            """)
        output_data = dictfetchall(cursor)

        return output_data
def get_custom_videos(params):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                            v.video_id, 
                            v.user_id_id, 
                            v.video_title,
                            u.first_name, 
                            u.last_name,
                            u.image,
                            v.video_thumbnail
                        FROM 
                            public.profile_page_videodetails v
                        LEFT JOIN
                            public.profile_page_userdetails u
                        USING
                            (user_id_id)
                        WHERE
                            v.video_id 
                        IN
                            %(l)s
                            """,params)
        output_data = dictfetchall(cursor)

    return output_data
def get_history_videos(params):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                            v.video_id, 
                            v.user_id_id, 
                            v.video_title,
                            u.first_name, 
                            u.last_name,
                            u.image,
                            v.video_thumbnail
                        FROM 
                            public.profile_page_videodetails v
                        LEFT JOIN
                            public.profile_page_userdetails u
                        USING
                            (user_id_id)
                        LEFT JOIN
                            public.profile_page_history h
                        ON
                            v.video_id = h.video_id_id
                        WHERE
                            v.video_id 
                        IN
                            %(l)s
                        ORDER BY
                            h.created_at desc
                            """,params)
        output_data = dictfetchall(cursor)
    return output_data

def get_custom_subscriptions(params):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                            v.video_id, 
                            v.user_id_id, 
                            v.video_title,
                            u.first_name, 
                            u.last_name,
                            u.image,
                            v.video_thumbnail
                        FROM 
                            public.profile_page_videodetails v
                        LEFT JOIN
                            public.profile_page_userdetails u
                        USING
                            (user_id_id)
                        WHERE
                            v.user_id_id 
                        IN
                            %(l)s
                        ORDER BY 
                            v.video_id desc
                            """,params)
        output_data = dictfetchall(cursor)

    return output_data

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
