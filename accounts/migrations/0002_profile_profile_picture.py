# Generated by Django 5.1.7 on 2025-03-23 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_dp.png', null=True, upload_to='images/'),
        ),
    ]
