# Generated by Django 2.2 on 2023-01-05 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile_page', '0008_videodetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videodetails',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_page.UserDetails'),
        ),
    ]
