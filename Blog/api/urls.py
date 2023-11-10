from django.urls import path
from .views import UserDetailAPI,RegisterUserAPIView,user_login,CreatePostView,GetPostView,PostCommentView
urlpatterns = [
    path("get-details/",UserDetailAPI.as_view()),
    path('register/',RegisterUserAPIView.as_view()),
    path('create_post/',CreatePostView.as_view()),
    path('get_blog_posts/',GetPostView.as_view()),
    path('create_post_comment/',PostCommentView.as_view()),
    path('login/', user_login, name='login'),
]