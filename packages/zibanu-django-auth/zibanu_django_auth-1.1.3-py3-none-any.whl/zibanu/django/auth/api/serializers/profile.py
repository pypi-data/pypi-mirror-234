# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         27/04/23 6:58
# Project:      Zibanu - Django
# Module Name:  profile
# Description:
# ****************************************************************
from django.conf import settings
from zibanu.django.rest_framework import serializers
from zibanu.django.auth.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    """
    UserProfile entity serializer.
    """
    width = settings.ZB_AUTH_AVATAR_SIZE
    height = settings.ZB_AUTH_AVATAR_SIZE
    represent_in_base64 = settings.ZB_AUTH_AVATAR_BASE64
    avatar = serializers.HybridImageField(max_length=None, required=False, allow_null=False,
                                          represent_in_base64=represent_in_base64, image_width=width,
                                          image_height=height)

    class Meta:
        """
        ProfileSerializer Metaclass
        """
        model = UserProfile
        fields = (
            "timezone", "theme", "lang", "avatar", "messages_timeout", "keep_logged_in", "app_profile",
            "multiple_login", "secure_password"
        )
