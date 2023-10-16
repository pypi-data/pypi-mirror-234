# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         7/06/23 14:42
# Project:      Zibanu - Django
# Module Name:  group
# Description:
# ****************************************************************
from django.contrib.auth.models import Group
from zibanu.django.rest_framework import serializers


class GroupListSerializer(serializers.ModelSerializer):
    """
    Group entity list serializer
    """

    class Meta:
        """
        GroupListSerializer metaclass
        """
        model = Group
        fields = ("id", "name")