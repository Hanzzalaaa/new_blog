from django.db import models
from django.contrib.auth.models import User
import os,random
from datetime import datetime ,date
from django.conf import settings


# Create your models here.
def save_media(instance, filename):
    file_extension = os.path.splitext(filename)[1].lstrip('.')
    random_number = random.randint(0, 99)
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')+str(random_number)+str(random_number)
    target_dir = f'media/{instance.pk}/media'
    file_dir = os.path.join(settings.MEDIA_ROOT, target_dir)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir, 0o777)
    return os.path.join(target_dir, f'{current_datetime}.{file_extension}')


class Post(models.Model):
    i_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='post_of_user')
    title = models.CharField(max_length=120)
    discription = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    # def __str__(self) -> str:
    #     return "%s - %s" %(self.title)


class Comment(models.Model):
    i_user = models.ForeignKey(User,on_delete = models.CASCADE, related_name='comment_of_user')
    i_post = models.ForeignKey(Post,on_delete = models.CASCADE, related_name='post_of_comment')
    comment_text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "%s - %s" %(self.i_user.pk,self.i_post.pk)


class PostMedia(models.Model):
    i_post = models.ForeignKey(Post,on_delete = models.CASCADE, related_name='image_of_post')
    media = models.FileField(max_length=256, upload_to = save_media, null=True, blank=True)

    def __str__(self) -> str:
        return "%s - %s" %(self.i_post,self.media.url)



