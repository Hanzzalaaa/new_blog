# Generated by Django 4.2.7 on 2023-11-10 09:32

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('discription', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('i_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_of_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(blank=True, max_length=256, null=True, upload_to=api.models.save_media)),
                ('i_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_of_post', to='api.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('i_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_of_comment', to='api.post')),
                ('i_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_of_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
