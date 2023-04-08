from django.shortcuts import render, redirect
from profile_page.models import UserDetails, VideoDetails
from profile_page import views as home_views
from django.db import connection


def search(request):

    if request.method == "GET":

        search_text = request.GET["search_text"]

        filtered_users = UserDetails.objects.filter(
            first_name__icontains=search_text) | UserDetails.objects.filter(last_name__icontains=search_text)
        filtered_videos = VideoDetails.objects.filter(
            video_title__icontains=search_text) | VideoDetails.objects.filter(video_description__icontains=search_text)
        obj = UserDetails.objects.get(user_id=request.user.id)
        custom = custom_sql(search_text)
        context = {
            'filtered_users': filtered_users,
            'filtered_videos': filtered_videos,
            'video_uploader': custom,
            'user_details': obj,
        }
        return render(request, 'search_page.html', context)


def custom_sql(search_text):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                            v.video_id, 
                            v.user_id_id, 
                            v.video_title,
                            v.video_description,
                            u.first_name, 
                            u.last_name,
                            u.image,
                            v.video_thumbnail
                        FROM 
                            public.profile_page_videodetails v
                        LEFT JOIN
                            public.profile_page_userdetails u
                        using
                            (user_id_id)
                        WHERE 
                            v.video_title 
                            ILIKE
                                %(search_text)s 
                            OR
                            v.video_description
                            ILIKE
                                %(search_text)s
                            """, {'search_text': '%{}%'.format(search_text)})

        output_data = dictfetchall(cursor)

        return output_data


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
