# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The home page
    path("<str:newuser>", views.BasePageView.as_view(), name="home"),
    path("", views.BasePageView.as_view(), name="home"),
]
