# Generated by Django 2.2 on 2023-01-04 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_page', '0004_auto_20230104_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
