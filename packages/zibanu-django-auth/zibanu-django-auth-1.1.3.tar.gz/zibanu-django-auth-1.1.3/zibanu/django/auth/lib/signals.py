# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         13/05/23 11:59
# Project:      Zibanu - Django
# Module Name:  signals
# Description:
# ****************************************************************
"""
Signal definitions for associate to events
"""
from django import dispatch
from django.apps import apps
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from typing import Any
from zibanu.django.utils import get_ip_address

on_change_password = dispatch.Signal()
on_request_password = dispatch.Signal()

@receiver(on_change_password, dispatch_uid="on_change_password")
@receiver(on_request_password, dispatch_uid="on_request_password")
@receiver(user_logged_in, dispatch_uid="on_user_logged_in")
@receiver(user_login_failed, dispatch_uid="on_user_login_failed")
def auth_event(sender: Any, user: Any = None, **kwargs) -> None:
    """
    Signal for change password or request password events

    Parameters
    ----------
    sender: Sender class of signal
    user: User object to get data
    kwargs: Dictionary with fields and parametes

    Returns
    -------
    None
    """
    # Set detail field
    detail = kwargs.get("detail", "")
    if kwargs.get("credentials", None) is not None:
        detail = kwargs.get("credentials").get("username", "")

    if isinstance(sender, str):
        class_name = sender
    else:
        class_name = sender.__name__
    ip_address = get_ip_address(kwargs.get("request", None))
    # Try to capture receiver name from receivers pool.
    try:
        receivers = kwargs.get("signal").receivers
        receiver_id = receivers[len(receivers)-1][0][0]
        if isinstance(receiver_id, str):
            action = receiver_id
        else:
            action = "zb_auth_event"
        # If username context var exists.
    except:
        action = "zb_auth_event"


    if apps.is_installed("zibanu.django.logging"):
        from zibanu.django.logging.models import Log
        log = Log(user=user, sender=class_name, action=action, ip_address=ip_address, detail=detail)
        log.save()


