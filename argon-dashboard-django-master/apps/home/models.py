# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


VARIANT = (
    ('a','a'),
    ('b','b'),
    ('d','d'),
    ('c','c'),
)

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
    is_edit = models.ManyToManyField(User, related_name='edit_sers')

class Quetions_list(models.Model):
    quetions = models.ForeignKey(Quetions,on_delete=models.CASCADE, related_name='quetions_list')
    title = models.CharField(max_length=400)
    a=models.CharField(max_length=400)
    b=models.CharField(max_length=400)
    d=models.CharField(max_length=400)
    c=models.CharField(max_length=400)
    
    true_ansver = models.CharField(choices=VARIANT, max_length=40)


