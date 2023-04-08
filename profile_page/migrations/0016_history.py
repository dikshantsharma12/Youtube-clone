# Generated by Django 2.2 on 2023-01-11 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile_page', '0015_auto_20230110_0532'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_user', to='profile_page.UserDetails')),
                ('video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_videos', to='profile_page.VideoDetails')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
