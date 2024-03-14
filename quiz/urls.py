from django.urls import path,include
from .views import *
urlpatterns = [
    path('', homepage),
    path('d/', dd),
    path('add_result/', add_result),
    path('page/<str:url>/', detail),
    path('quiz_signle/<str:url>/', quiz_single),
    path('page/<str:url>/<str:url2>/', is_detail),
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('create_quiz/', create_quiz, name='create_quiz'),
    path('quetions_list_remove/<str:url>/', quetions_list_remove, name='quetions_list_remove'),
    path('quetions_list_update/<str:url>/', quetions_list_update, name='quetions_list_update'),
    path('quetions_list_create/', quetions_list_create, name='quetions_list_create'),

]
