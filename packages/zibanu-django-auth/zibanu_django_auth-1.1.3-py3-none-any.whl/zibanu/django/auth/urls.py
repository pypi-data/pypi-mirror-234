# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         8/04/23 7:32
# Project:      Django Plugins
# Module Name:  urls
# Description:
# ****************************************************************
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainSlidingView
from rest_framework_simplejwt.views import TokenRefreshSlidingView
from zibanu.django.auth.api.services import GroupService
from zibanu.django.auth.api.services import LogoutUser
from zibanu.django.auth.api.services import PermissionService
from zibanu.django.auth.api.services import ProfileService
from zibanu.django.auth.api.services import UserService

"""
URL patterns for zibanu.django.auth package
"""

urlpatterns = [
    path("login/", TokenObtainSlidingView.as_view(), name="token_obtain"),
    path("logout/", LogoutUser.as_view({"post": "logout"}), name="Logout user endpoint"),
    path("refresh/", TokenRefreshSlidingView.as_view(), name="token_refresh"),
    path("change-password/", UserService.as_view({"post": "change_password"}), name="change_password"),
    path("request-password/", UserService.as_view({"post": "request_password"}), name="request_password"),
    path("group/list/", GroupService.as_view({"post": "list"}), name="list_groups"),
    path("permission/list/", PermissionService.as_view({"post": "list"}), name="list_permissions"),
    path("profile/update/", ProfileService.as_view({"post": "update"}), name="update_profile"),
    path("user/add/", UserService.as_view({"post": "create"}), name="add_user"),
    path("user/delete/", UserService.as_view({"post": "destroy"}), name="delete_user"),
    path("user/list/", UserService.as_view({"post": "list"}), name="list_users"),
    path("user/update/", UserService.as_view({"post": "update"}), name="update_user")
]