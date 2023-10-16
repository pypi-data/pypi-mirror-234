# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         8/04/23 7:18
# Project:      Django Plugins
# Module Name:  apps
# Description:
# ****************************************************************
from django.apps import apps
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ZbDjangoAuth(AppConfig):
    """
    Inherited class from django.apps.AppConfig to define configuration of zibanu.django.auth app.
    """
    default_auto_field = "django.db.models.AutoField"
    name = "zibanu.django.auth"
    verbose_name = _("Zibanu Auth for Django")
    label = "zb_auth"

    def ready(self):
        """
        Override method used for django application loader after the application has been loaded successfully.

        Returns
        -------
        None

        Settings
        -------
        ZB_AUTH_INCLUDE_GROUPS: If True, includes the set of groups to which the user belongs, False ignores them. Default: True
        ZB_AUTH_INCLUDE_PERMISSIONS: If True, includes the set of permissions the user has, False ignores them. Default: False
        ZB_AUTH_CHANGE_PASSWORD_TEMPLATE: Template used to generate password change confirmation email. Default: "on_change_password"
        ZB_AUTH_REQUEST_PASSWORD_TEMPLATE: Template used to generate request password email. Default: "on_request_password"
        ZB_AUTH_ALLOW_MULTIPLE_LOGIN: If True, allows a user to have multiple access from the same type of application, False only allows one access. Default is FALSE
        """
        # Import signals
        import zibanu.django.auth.lib.signals
        # Set default settings for Simple JWT Module
        settings.ZB_AUTH_INCLUDE_GROUPS = getattr(settings, "ZB_AUTH_INCLUDE_GROUPS", True)
        settings.ZB_AUTH_INCLUDE_PERMISSIONS = getattr(settings, "ZB_AUTH_INCLUDE_PERMISSIONS", False)
        settings.ZB_AUTH_CHANGE_PASSWORD_TEMPLATE = getattr(settings, "ZB_AUTH_CHANGE_PASSWORD_TEMPLATE", "change_password")
        settings.ZB_AUTH_REQUEST_PASSWORD_TEMPLATE = getattr(settings, "ZB_AUTH_REQUEST_PASSWORD_TEMPLATE", "request_password")
        settings.ZB_AUTH_ALLOW_MULTIPLE_LOGIN = getattr(settings, "ZB_AUTH_ALLOW_MULTIPLE_LOGIN", False)
        settings.ZB_AUTH_AVATAR_BASE64 = getattr(settings, "ZB_AUTH_AVATAR_FORMAT", True)
        settings.ZB_AUTH_AVATAR_SIZE = getattr(settings, "ZB_AUTH_AVATAR_SIZE", 0)
