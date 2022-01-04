"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
from itertools import chain

from django.contrib import admin
from django.urls import include, path

from .user.urls import urlpatterns as user_urls
from .vue_api.urls import urlpatterns as vue_api_urls

api_urlpatterns = list(chain.from_iterable([user_urls, vue_api_urls]))

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns)),
    path("", include("backend.vue_api.urls")),
]
