# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # The second page
    path('index2/', views.index2, name='index2'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
