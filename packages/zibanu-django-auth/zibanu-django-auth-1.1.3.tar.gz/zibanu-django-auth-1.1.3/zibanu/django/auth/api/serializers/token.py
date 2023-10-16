# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         27/04/23 7:02
# Project:      Zibanu - Django
# Module Name:  token
# Description:
# ****************************************************************
import logging
import traceback
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import user_logged_in, user_login_failed
from django.contrib.auth.models import update_last_login
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenRefreshSlidingSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import SlidingToken, RefreshToken
from typing import Dict, Any
from zibanu.django.auth.api.serializers.user import UserTokenSerializer
from zibanu.django.auth.lib.utils import get_cache_key
from zibanu.django.utils import get_http_origin, get_ip_address


class EmailTokenObtainSerializer(TokenObtainSerializer):
    """
    SimpleJWTToken serializer to get token with full user object payload for email authentication method.
    """
    username_field = get_user_model().EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        """
        Constructor method for EmailTokenObtainSerializer Class

        Parameters
        ----------
        *args: Single tuple of parameters values
        **kwargs: Dictionary with key - value of parameters.
        """
        super().__init__(*args, **kwargs)
        self.__request = self.context.get("request")
        self.__key_suffix = get_http_origin(self.context.get("request"), md5=True)
        self.__close_sessions = self.context.get("request").data.pop("close", False)
        self.error_messages["multiple_login"] = _("The user does not have allowed multiple login. Please close previous sessions.")
        self.error_messages["invalid_user"] = _("The token does not have associated user.")
        self.error_messages["invalid_profile"] = _("The user does not have associated profile.")
        self.error_messages["not_controlled"] = _("Critical Error! Not controlled exception.")
        self.user = None

    @property
    def close_sessions(self):
        """
        Property to view if request has close sessions flag active.

        Returns
        -------
        close_sessions: boolean: True if close previous session, otherwise False or None
        """
        return  self.__close_sessions

    def _validate_sessions(self, user):
        """
        Method to validate if the user has another open session. If request data parameter close is True, create new
        session and close others.

        Parameters
        ----------
        user: User object representation.

        Returns
        -------
        None
        """
        log_params = {
            "ip_address": get_ip_address(self.context.get("request")),
            "user_id": user.id
        }
        try:
            if hasattr(user, "profile"):
                if not user.profile.multiple_login:
                    cache_key = get_cache_key(self.__request, user)
                    cached_token = cache.get(cache_key, None)
                    if self.close_sessions and cached_token is not None:
                        cached_token.blacklist()
                        cache.delete(cache_key)
                    else:
                        if cached_token is not None:
                            raise AuthenticationFailed(self.error_messages["multiple_login"])
            else:
                raise AuthenticationFailed(self.error_messages["invalid_profile"])
        except AuthenticationFailed as exc:
            logging.critical(exc.detail, log_params)
            raise AuthenticationFailed(exc.detail) from exc
        except Exception as exc:
            logging.critical(str(exc), log_params)
            logging.debug(traceback.format_exc(), log_params)
            raise AuthenticationFailed(self.error_messages["not_controlled"])

    def _save_cache(self, token: Any) -> str:
        """
        Method to save the token in cache if multiple_login are not allowed.

        Parameters
        ----------
        token: Token object

        Returns
        -------
        String with token
        """
        # Validate cache if required
        if self.user.profile is not None and not self.user.profile.multiple_login:
            cache.set(get_cache_key(self.__request, self.user), token, timeout=token.lifetime.total_seconds())
        return str(token)

    @classmethod
    def get_token(cls, user):
        """
        Get JWT token including full user object data

        Parameters
        ----------
        user: User object to serialize

        Returns
        -------
        token: SlidingToken object
        """
        token = super().get_token(user)

        # Include user data
        user_serializer = UserTokenSerializer(instance=user)
        token["user"] = user_serializer.data
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        """
        Serializer validate method to validate user object from attrs parameter

        Parameters
        ----------
        attrs: Request dictionary attributes

        Returns
        -------
        None: Empty data
        """
        user = get_user_model().objects.filter(email__iexact=attrs.get(self.username_field)).first()

        if user is None:
            user_login_failed.send(self.__class__, user=None, request=self.context.get("request"),
                                   detail=attrs.get(self.username_field))
            raise AuthenticationFailed(self.error_messages["no_active_account"], "no_active_account")
        self._validate_sessions(user)
        authenticate_kwargs = {
            get_user_model().USERNAME_FIELD: user.get_username(),
            "password": attrs.get("password")
        }

        self.user = authenticate(**authenticate_kwargs)
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        return {}


class EmailTokenObtainSlidingSerializer(EmailTokenObtainSerializer):
    """
    TokenSlidingSerializer child class of EmailTokenObtainSerializer
    """
    token_class = SlidingToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        """
        Serializer validate method to validate user object from request attributes

        Parameters
        ----------
        attrs: Request dictionary attributes

        Returns
        -------
        data: SlidingToken object with full user object data
        """
        data = super().validate(attrs)
        token = self.get_token(self.user)
        data["token"] = self._save_cache(token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        user_logged_in.send(sender=self.__class__, user=self.user, request=self.context.get("request"))
        return data


class EmailTokenRefreshSlidingSerializer(TokenRefreshSlidingSerializer):
    """
    EmailTokenRefreshSlidingSerializer child class from TokenRefreshSlidingSerializer
    that implements validation from cached tokens and store a new token in cache.
    """


    def __init__(self, *args, **kwargs):
        """
        Override method to set a new message for invalid token.

        Parameters
        ----------
        *args: Single tuple of parameters values
        **kwargs: Dictionary with key/value of parameters.
        """
        super().__init__(*args, **kwargs)
        self.__request = self.context.get("request")
        self.error_messages["invalid_token"] = _("You're trying to refresh and invalid token.")

    def __get_user(self, token: SlidingToken):
        user_id = token.payload.get("user_id")
        user = None
        try:
            user = get_user_model().objects.get(pk=user_id)
        except ObjectDoesNotExist:
            user = None
        finally:
            return user


    def validate(self, attrs):
        """
        Override method to implement a cached token validation and new token generation.

        Parameters
        ----------
        attrs: Set of attributes for token generation

        Returns
        -------
        Dictionary with "token" key and new token value.
        """
        token = self.token_class(attrs["token"])
        token.check_exp(api_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

        # Load user from token and generate cache key
        user = self.__get_user(token)
        if user is None:
            raise AuthenticationFailed(self.error_messages["invalid_user"])
        cache_key = get_cache_key(self.__request, user)

        # Validate if multiple login flag is active
        if not user.profile.multiple_login:
            cached_token = cache.get(cache_key, None)
            if cached_token is None:
                raise AuthenticationFailed(self.error_messages["invalid_token"])
            else:
                cached_token.blacklist()

        # Generate new token
        token = SlidingToken.for_user(user)
        user_serializer = UserTokenSerializer(instance=user)
        token["user"] = user_serializer.data

        # Set new token in cache if multiple login flag is active
        if not user.profile.multiple_login:
            cache.set(cache_key, token, timeout=token.lifetime.total_seconds())

        return {"token": str(token)}