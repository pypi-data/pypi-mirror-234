# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         27/04/23 6:57
# Project:      Zibanu - Django
# Module Name:  user
# Description:  Set of serializers for user entity
# ****************************************************************
from .profile import ProfileSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from zibanu.django.auth.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for Django user entity, including user profile, permissions and roles (groups).
    """
    full_name = serializers.SerializerMethodField(default="Guest")
    profile = ProfileSerializer(required=True, read_only=False)
    roles = serializers.SerializerMethodField(default=[])
    permissions = serializers.SerializerMethodField(default=[])

    def get_permissions(self, instance) -> list:
        """
        Method to get permission list from User object.

        Parameters
        ----------
        instance: User object instance

        Returns
        -------
        permissions: Permission list

        """
        permissions = []
        if self.context.get("load_permissions", settings.ZB_AUTH_INCLUDE_PERMISSIONS):
            for permission in instance.user_permissions.all():
                permissions.append(permission.name)
        return permissions

    def get_roles(self, instance) -> list:
        """
        Method to get groups list from User object

        Parameters
        ----------
        instance: User object instance

        Returns
        -------
        groups: Group list

        """
        roles = []
        if self.context.get("load_roles", settings.ZB_AUTH_INCLUDE_GROUPS):
            for group in instance.groups.all():
                roles.append(group.name)
        return roles

    def get_full_name(self, instance) -> str:
        """
        Method to get full name from user object instance

        Parameters
        ----------
        instance: User object instance

        Returns
        -------
        full_name: String with user full name
        """
        return instance.get_full_name()

    def create(self, validated_data) -> object:
        """
        Create a user object including its user profile.

        Parameters
        ----------
        validated_data: Validated data dictionary from serializer

        Returns
        -------
        use_object: User object created if successfully
        """
        email = validated_data.pop("email")
        user_object = self.Meta.model.objects.filter(email__exact=email).first()

        if user_object is None:
            if "password" not in validated_data.keys():
                raise ValidationError(_("The password is required."), "create_user")

            password = validated_data.pop("password")
            username = validated_data.pop("username")
            profile_data = validated_data.pop("profile")
            user_object = self.Meta.model.objects.create_user(username=username, email=email, password=password, **validated_data)
            # Create profile
            user_profile = UserProfile(user=user_object, **profile_data)
            user_profile.save()
        else:
            raise ValidationError(_("Email is already registered in our database."))
        return user_object

    class Meta:
        """
        UserSerializer metaclass
        """
        model = get_user_model()
        fields = ("email", "full_name", "last_login", "is_staff", "is_superuser", "is_active", "profile", "roles",
                  "first_name", "last_name", "permissions", "username", "password")


class UserListSerializer(serializers.ModelSerializer):
    """
    User entity list serializer
    """
    full_name = serializers.SerializerMethodField(default="Guest")

    class Meta:
        """
        UserListSerializer metaclass
        """
        fields = ("full_name", "email", "last_login", "is_staff", "is_superuser", "id", "first_name", "last_name")
        model = get_user_model()

    def get_full_name(self, instance) -> str:
        """
        Method to get full name from user object instance

        Parameters
        ----------
        instance: User object instance

        Returns
        -------
        full_name: String with user full name
        """
        return instance.get_full_name()

class UserTokenSerializer(UserSerializer):
    """
    Class inherited from UserSerializer to only use in the TokenSerializer for the authentication process.
    """
    class Meta:
        model = get_user_model()
        fields = ("email", "is_staff", "is_superuser", "username", "profile", "roles", "permissions")
