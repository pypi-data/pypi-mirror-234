# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         13/05/23 10:23
# Project:      Zibanu - Django
# Module Name:  utils
# Description:  Utils tools for auth module
# ****************************************************************
from django.contrib.auth.models import User
from rest_framework.request import Request
from typing import Any
from zibanu.django.utils import get_http_origin
from zibanu.django.utils import get_user as zb_get_user


def get_user(user: Any) -> Any:
    """
    Function to get user object from SimpleJWT TokenUser.

    Parameters
    ----------
    user: User object of SimpleJWT Token User type, or User object type

    Returns
    -------
    user: Django user object type
    """
    return zb_get_user(user=user)


def get_cache_key(request: Request, user: Any) -> str:
    """
    Function to construct a cache key from http_origin and username

    Parameters
    ----------
    request: Request object from HTTP
    user: User object

    Returns
    -------
    cache_key: str: Cache key to set or get.
    """
    return user.username + "." + get_http_origin(request, md5=True)