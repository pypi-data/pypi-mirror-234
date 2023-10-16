# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         19/06/23 10:52
# Project:      Zibanu - Django
# Module Name:  permission
# Description:
# ****************************************************************
from django.contrib.auth.models import Permission
from zibanu.django.rest_framework import serializers

class PermissionSerializer(serializers.ModelSerializer):
    """
    Permission entity serializer
    """

    class Meta:
        """
        PermissionSerializer metaclass
        """
        model = Permission
        fields = ("id", "name")