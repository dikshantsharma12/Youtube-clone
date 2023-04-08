from django.shortcuts import render ,redirect
from profile_page.models import UserDetails, VideoDetails, Follow, History
from .models import LikedVideos, SavedVideos, UnsavedVideos, Comments
from django.http import JsonResponse
import json
from django.db import connection
from profile_page.views import subscribe
import re

# Create your views here.


def toggle_like(request):
    request_data = json.loads(request.body)
    request_video_id = int(request_data['videoId'])
    request_user_id = int(request_data['userId'])
    option = request_data['option']
    user_id = UserDetails.objects.get(user_id=request_user_id)
    video_id = VideoDetails.objects.get(video_id=request_video_id)
    update_like =VideoDetails.objects.get(video_id=request_video_id)
    update_dislike =VideoDetails.objects.get(video_id=request_video_id)

    if option == "like-button":

        
        update_like.video_likes = update_like.video_likes +1
        update_like.save()

        try:
            UnsavedVideos.objects.get(
                user_id=user_id, disliked_videos=video_id).delete()
            update_dislike.video_dislikes -= 1
            update_dislike.save()

            SavedVideos.objects.create(
                user_id=user_id, liked_videos=video_id).save()
            return JsonResponse({
                'removedDislike': True,
                'liked': True
            })
        except Exception as e:
            print(e)
            SavedVideos.objects.create(
                user_id=user_id, liked_videos=video_id).save()
            return JsonResponse({
                "liked": True
            })
    if option == "dislike-button":
        
        try:
            SavedVideos.objects.get(
                user_id=user_id, liked_videos=video_id).delete()

            update_like.video_likes = update_like.video_likes - 1
            update_like.save()

            UnsavedVideos.objects.create(
                user_id=user_id, disliked_videos=video_id).save()

            update_dislike.video_dislikes += 1
    
            update_dislike.save()

            return JsonResponse({
                'removedLike': True,
                'disliked': True
            })
        except Exception as e:
            print(e)
            UnsavedVideos.objects.create(
                user_id=user_id, disliked_videos=video_id).save()
            
            update_dislike.video_dislikes += 1
            update_dislike.save()

            return JsonResponse({
                "disliked": True
            })
    if option == "already-liked":

        update_like.video_likes = update_like.video_likes - 1
        update_like.save()

        SavedVideos.objects.get(
            user_id=user_id, liked_videos=video_id).delete()
        return JsonResponse({
            'removeLike': True
        })

    if option == "already-disliked":
        UnsavedVideos.objects.get(
            user_id=user_id, disliked_videos=video_id).delete()
            
        update_dislike.video_dislikes -= 1
        update_dislike.save()

        return JsonResponse({
            'removeDislike': True
        })


def save_video(request):

    request_data = json.loads(request.body)
    request_video_id = int(request_data['videoId'])
    request_user_id = int(request_data['userId'])
    user_id = UserDetails.objects.get(user_id=request_user_id)
    video_id = VideoDetails.objects.get(video_id=request_video_id)

    try:
        LikedVideos.objects.get(saved_videos=video_id,
                                user_id=user_id).delete()
        return JsonResponse({
            'status': 'removed'
        })
    except:
        LikedVideos.objects.create(
            saved_videos=video_id, user_id=user_id).save()
        return JsonResponse({
            'status': 'saved'
        })


def video_page(request, video_id):
    """Video Page"""

    videos = VideoDetails.objects.all()

    curr_video = VideoDetails.objects.get(video_id=video_id)

    # VIEW PART

    video_views = VideoDetails.objects.get(video_id=video_id)
    video_views.video_views = video_views.video_views + 1
    video_views.save()

    # HISTORY PART
    watcher_id = request.user.id
    watcher = UserDetails.objects.get(user_id=watcher_id)
    try:
        History.objects.get(user_id=watcher, video_id=curr_video).delete()
        History.objects.create(user_id=watcher, video_id=curr_video).save()
    except:
        History.objects.create(user_id=watcher, video_id=curr_video).save()

    # CURRENT VIDEO

    curr_user_details = VideoDetails.objects.filter(video_id=video_id)
    curr_user = UserDetails.objects.get(user_id=curr_user_details[0].user_id)

    # COMMENTS PART
    curr_video_commments = sql_curr_comment(video_id)

    custom = custom_sql()

    commenter_id = request.user.id

    if request.method == "POST":
        Comments.objects.create(
            commenter=UserDetails.objects.get(user_id=commenter_id),
            video=curr_video,
            comment=request.POST["comment"]
        ).save()
        curr_video.video_comments += 1
        curr_video.save()
        return redirect(f"/{video_id}")

    try:
        LikedVideos.objects.get(saved_videos=video_id, user_id=request.user.id)
        already_saved = True
    except:
        already_saved = False

    if request.user.is_authenticated:
        user_details = UserDetails.objects.get(user_id=request.user.id)
        is_followed = False
        try:
            is_followed = Follow.objects.get(
                followee=request.user.id, follower=int(curr_user_details[0].user_id))
        except:
            print("User Not Found")

        already_liked = False
        already_disliked = False

        try:
            SavedVideos.objects.get(
                user_id=request.user.id, liked_videos=video_id)
            already_liked = True
        except Exception as e:
            print('No Data Found...', e)
        try:
            UnsavedVideos.objects.get(
                user_id=request.user.id, disliked_videos=video_id)
            already_disliked = True
        except Exception as e:
            print('No Data Found...', e)

        context = {
            'user_details': user_details,
            'videos': videos,
            'curr_video': curr_video,
            'user_data': custom,
            'curr_user': curr_user,
            'already_followed': is_followed,
            'already_saved': already_saved,
            'already_liked': already_liked,
            'already_disliked': already_disliked,
            'comments': curr_video_commments
        }
        return render(request, 'video_page.html', context)
    else:

        videos = VideoDetails.objects.all()
        context = {
            'videos': videos,
            'curr_video': curr_video,
            'user_data': custom,
            'curr_user': curr_user,
        }
        return render(request, 'video_page.html', context)


def custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                            v.video_id, 
                            v.user_id_id, 
                            v.video_title,
                            u.first_name, 
                            u.last_name,
                            u.image,
                            v.video_thumbnail,
                            v.video_comments
                        FROM 
                            public.profile_page_videodetails v
                        LEFT JOIN
                            public.profile_page_userdetails u
                        using
                            (user_id_id)
                            """)
        output_data = dictfetchall(cursor)
        return output_data


def sql_curr_comment(video_id):

    with connection.cursor() as cursor:
        cursor.execute("""  SELECT 
                                u.first_name,
                                u.last_name,
                                u.image,
                                c.comment
                            FROM 
                                public.profile_page_userdetails u
                            LEFT JOIN
                                public.video_page_comments c
                            ON
                                c.commenter_id = u.user_id_id
                            WHERE
                                c.video_id = {}
                            ORDER BY
                                c.created_at desc
        """.format(video_id))

        output_data = dictfetchall(cursor)
        return output_data


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
