from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ['i_user', 'title', 'discription', 'created']

@admin.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['i_user', 'i_post', 'comment_text', 'created']

@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ['i_post', 'media']