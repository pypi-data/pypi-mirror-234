# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         7/06/23 14:39
# Project:      Zibanu - Django
# Module Name:  groups
# Description:
# ****************************************************************
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from zibanu.django.auth.api.serializers import GroupListSerializer
from zibanu.django.rest_framework.decorators import permission_required
from zibanu.django.rest_framework.viewsets import ModelViewSet


class GroupService(ModelViewSet):
    """
    Set of REST service for Group Model
    """
    model = Group
    serializer_class = GroupListSerializer

    @method_decorator(permission_required(("is_staff", "auth.view_group")))
    def list(self, request, *args, **kwargs) -> Response:
        """
        REST service to list groups

        Parameters
        ----------
        request: HTTP request object
        *args: Tuple of parameters
        **kwargs: Dictionary of parameters

        Returns
        -------
        response: Response object with HTTP status and list of dataset.
        """
        return super().list(request, *args, **kwargs)

    @method_decorator(permission_required(("is_staff", "auth.add_group")))
    def create(self, request, *args, **kwargs) -> Response:
        """
        REST service to create a group

        Parameters
        ----------
        request: HTTP request object
        *args: Tuple of parameters
        **kwargs: Dictionary of parameters

        Returns
        -------
        response: Response object with HTTP status and object dataset. Status 201 if success.
        """
        return super().create(request, *args, **kwargs)