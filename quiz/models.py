from django.db import models
from django.contrib.auth.models import User
import uuid

VARIANT = (
    ('a','a'),
    ('b','b'),
    ('d','d'),
    ('c','c'),
)

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
#     bio = models.TextField()

#     def __str__(self):
#         return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField()


class Quetions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    categorys = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='quiz_category')
    title = models.CharField(max_length=400)
    body = models.TextField()
    duraction_time =models.IntegerField(default=0)
    date = models.DateField( auto_now_add=True)
    is_edit = models.ManyToManyField(User, related_name='edit_sers',blank=True)
    using_users = models.ManyToManyField(User, related_name='using_users',blank=True)
    random_url = models.UUIDField(default=uuid.uuid4)
    # is_show = models.BooleanField()

class Result(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quetions,on_delete=models.CASCADE , related_name='result')
    true =models.IntegerField(default=0)
    false =models.IntegerField(default=0)
    using_count =models.IntegerField(default=0)
    time = models.CharField(max_length=400)



class Quetions_list(models.Model):
    quetions = models.ForeignKey(Quetions,on_delete=models.CASCADE, related_name='quetions_list')
    title = models.CharField(max_length=400)
    a=models.CharField(max_length=400)
    b=models.CharField(max_length=400)
    d=models.CharField(max_length=400)
    c=models.CharField(max_length=400)
    true_ansver = models.CharField(choices=VARIANT, max_length=40)
    random_url = models.UUIDField(default=uuid.uuid4)

