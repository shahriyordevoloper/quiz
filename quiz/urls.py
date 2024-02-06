from django.urls import path,include
from .views import *
urlpatterns = [
    path('', homepage),
    path('page/<str:url>/', detail),
    path('page/<str:url>/<str:url2>', is_detail),

]
