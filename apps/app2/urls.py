# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.app2 import views

urlpatterns = [
    path('index2/<str:new_user>', views.Page1View.as_view(), name='index2'),
    path('index2/', views.Page1View.as_view(), name='index2'),
]
