
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
import magic
from django.db import transaction
from .models import *


# from django.contrib.auth.validators import UnicodeUsernameValidator

#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ["id", "first_name", "last_name", "username"]


#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=80,required=False)
    token = serializers.CharField(max_length=256,read_only=True)
    email = serializers.EmailField(
      required=True,
      validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
      write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
            'email', 'first_name', 'last_name','token')
        extra_kwargs = {
          'first_name': {'required': True},
          'last_name': {'required': True},
          # 'token': {'required': False,'read_only': True},
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
          raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
          username=validated_data['username'],
          email=validated_data['email'],
          first_name=validated_data['first_name'],
          last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        # Generate a token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Add the token to the response
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': token.key  # Include the token in the response
        }
        print(user_data,"++++++++++++++++++++++++++++++++")

        return user_data



class PostSerializer(serializers.Serializer):
    
    status_code = serializers.IntegerField(read_only=True, default=status.HTTP_400_BAD_REQUEST)
    status = serializers.BooleanField(read_only=True, default=False)
    message = serializers.CharField(read_only=True, default=None)
    data = serializers.DictField(read_only=True, default={})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resp = {'status': False, 'status_code': 400,
                     'message': None, 'data': {}}
        request = self.context.get("request")
        self.user = request.user
        self.fields["title"] = serializers.CharField(write_only=True, required=False)
        self.fields["discription"] = serializers.CharField(write_only=True, required=False)
        self.fields["image"] = serializers.ListField(
            child=serializers.FileField(),write_only=True, default=[], required=False)

    def validate(self, attrs):
        attrs['valid'] = True
        title = attrs.get('title')
        discription = attrs.get('discription')
        image = attrs.get("image",None)
        print(self.user,"++++++++++++++++")
        if not title:
            attrs['valid'] = False
            self.resp['message'] = "title is required"
            self.resp['status_code'] = status.HTTP_400_BAD_REQUEST
        
        elif not discription:
            attrs['valid'] = False
            self.resp['message'] = "discription is required"
            self.resp['status_code'] = status.HTTP_400_BAD_REQUEST

        elif image is not None:
            for media in image:
                file_type = magic.from_buffer(media.read(), mime=True).split("/")[0]
                if file_type not in ("image","video"):
                    attrs['valid'] = False
                    self.resp["message"] = f"{media.name} is not a valid media type."
                    break
                
        else:
            self.resp['message'] = "Validation successful"

        return attrs
            
            

    def create(self, validated_data):
      if validated_data['valid'] == True:
          title = validated_data.get('title')
          discription = validated_data.get('discription')
          media_lst = validated_data.get("image",[])

          with transaction.atomic():
              post_obj = Post.objects.create(
                                            i_user = self.user,
                                            title=title,
                                            discription = discription
              )
              
              self.resp['message'] = "Post without media created successfully"
              for media in media_lst:
                PostMedia.objects.create(media = media,
                                            i_post = post_obj)

                self.resp['message'] = "Post with media created successfully"
                  
              self.resp['status'] = True
              self.resp['status_code'] = status.HTTP_201_CREATED

      return self.resp
                    



class PostCommentSerializer(serializers.Serializer):
    status_code = serializers.IntegerField(read_only=True, default=status.HTTP_400_BAD_REQUEST)
    status = serializers.BooleanField(read_only=True, default=False)
    message = serializers.CharField(read_only=True, default=None)
    data = serializers.DictField(read_only=True, default={})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resp = {'status': False, 'status_code': 400,
                     'message': None, 'data': {}}
        request = self.context.get("request")
        self.user = request.user  
        self.fields["post_id"] = serializers.IntegerField(write_only=True, required=True)
        self.fields["text"] = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        attrs['valid'] = True
        post_id = attrs.get('post_id')
        text = attrs.get('text')
        post_obj = Post.objects.filter(pk=post_id)

        if not post_obj.exists:
          attrs['valid'] = False
          self.resp['message'] = "Post does not exist with id '{}'".format(post_id)
        else:
            attrs['post'] = post_obj.first()

        return attrs
    
    def create(self, validated_data):
      if validated_data['valid'] == True:
          Comment.objects.create(
              i_user = self.user,
              i_post = validated_data['post'],
              comment_text = validated_data['text']
          )
          self.resp['message'] = "Comment on Post created successfully"
          self.resp['status'] = True
          self.resp['status_code'] = status.HTTP_201_CREATED

      return self.resp

            