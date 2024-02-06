# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Quetions)
admin.site.register(Quetions_list)


