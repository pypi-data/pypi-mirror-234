# -*- coding: utf-8 -*-
# ****************************************************************
# IDE:          PyCharm
# Developed by: Mario Cerón Charry
# Date:         19/08/23 15:09
# Project:      Zibanu - Django
# Module Name:  auth
# Description:  
# ****************************************************************
import logging
import traceback
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from zibanu.django.auth.lib.utils import get_cache_key
from zibanu.django.rest_framework.viewsets import ViewSet
from zibanu.django.utils import get_user


class LogoutUser(ViewSet):
    """
    ViewSet to perform logout actions and remove cached tokens.
    """

    def logout(self, request, *args, **kwargs) -> Response:
        user = get_user(request.user)
        try:
            if not user.profile.multiple_login:
                cache_key = get_cache_key(request, user)
                token = cache.get(cache_key, None)
                if token is not None:
                    token.blacklist()
                cache.delete(cache_key)
        except Exception as exc:
            logging.error(str(exc))
            logging.debug(traceback.format_exc())
        finally:
            return Response(status=status.HTTP_200_OK)