# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         10/04/23 13:52
# Project:      Django Plugins
# Module Name:  models
# Description:
# ****************************************************************
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from timezone_utils.choices import ALL_TIMEZONES_CHOICES
from zibanu.django.db import models


class UserProfile(models.Model):
    """
    UserProfile model to store
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile",
                                related_query_name="user")
    timezone = models.CharField(max_length=50, null=False, blank=False, default="UTC",
                                choices=ALL_TIMEZONES_CHOICES, verbose_name=_("Time Zone"))
    theme = models.CharField(max_length=50, null=True, blank=False, verbose_name=_("User Theme"))
    lang = models.CharField(max_length=3, null=False, blank=False, default="en", verbose_name=_("Language"))
    avatar = models.ImageField(upload_to='profile_pics/', null=True, verbose_name=_("Avatar"))
    messages_timeout = models.IntegerField(default=10, null=False, blank=False, verbose_name=_("Message's Timeout"))
    keep_logged_in = models.BooleanField(default=False, null=False, blank=False, verbose_name=_("Keep Logged In"))
    multiple_login = models.BooleanField(default=False, null=False, blank=False, verbose_name=_("Allow multiple login"))
    secure_password = models.BooleanField(default=False, null=False, blank=False, verbose_name=_("Force secure password"))
    app_profile = models.JSONField(null=True, blank=False, verbose_name=_("Custom Application Profile"))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override method to force the flag multiple_login at user profile to False if is_staff attribute is False, and
        validate if ZB_AUTH_ALLOW_MULTIPLE_LOGIN setting is TRUE

        Parameters
        ----------
        force_insert: Force insert flag
        force_update: Force update flag
        using: Using database setting
        update_fields: Set of fields to update only.

        Returns
        -------
        None
        """
        if not settings.ZB_AUTH_ALLOW_MULTIPLE_LOGIN:
            if not self.user.is_staff:
                self.multiple_login = False
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)



    class Meta:
        db_table = "zb_auth_user_profile"
