# Blog

run pip install -r requirements.txt
run python manage.py makemigrations
run python manage.py migrate
run python manage.py runserver 8000


endpoint for signup
http://127.0.0.1:8000/register/
this is payload or json / keys  
username
password
password2
email
first_name
last_name

endpoint for signin
http://127.0.0.1:8000/login/
this is payload or json
''' {
    "username":"hanzala@gmail.com",
    "password":"Test@123"
    }
    '''

note:below apis hit in postman 
endpoint for create post 
http://127.0.0.1:8000/create_post/
this is payload or json
title:check
discription:for checking purpose
image (you add multiple images at a single hit)


endpoint for create comment on post 
http://127.0.0.1:8000/create_post_comment/
post_id:1
text:wow grape




endpoint for get all blogs with post , images and comments 
http://127.0.0.1:8000/get_blog_posts/


endpoint for get login user detail
http://127.0.0.1:8000/get-details/
