from django.urls import path,include
from .views import *
urlpatterns = [
    path('', homepage),
    path('d/', dd),
    path('add_result/', add_result),
    path('page/<str:url>/', detail),
    path('page/<str:url>/<str:url2>/', is_detail),
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),

]
