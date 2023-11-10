from django.forms import model_to_dict
from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics,status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *

# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



@api_view(['POST'])
def user_login(request):
    '''
    {
    "username":"hanzala@gmail.com",
    "password":"Adm1n@123"
    }
    '''
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,
                            'username':user.username,
                            'email':user.email,
                            'first name':user.first_name,
                            'last_name':user.last_name}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    



class CreatePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PostSerializer


class PostCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PostCommentSerializer

class GetPostView(APIView):
    def get(self,request):
        user_qs = User.objects.all()
        data_lst = []
        for user in user_qs:
            post_qs = Post.objects.filter(i_user = user)
            for post in post_qs:
                comment_qs = Comment.objects.filter(i_post = post).values('comment_text','i_user')
                comment_lst = []
                for comm in comment_qs:
                    comment_lst.append({
                        'comment':comm['comment_text'],
                        'commented_user':comm['i_user']
                    })
                media_lst = PostMedia.objects.filter(i_post = post).values_list('media' , flat = True)
                data = {
                    'post': model_to_dict(post),
                    'comments': comment_lst,
                    'media': media_lst
                }
                data_lst.append(data)

        return Response( {
            'status': True,
            'status_code': status.HTTP_200_OK,
            'message': 'All Blog Posts',
            'data': data_lst
        })