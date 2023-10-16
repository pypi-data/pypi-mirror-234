# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         19/06/23 14:29
# Project:      Zibanu - Django
# Module Name:  profile
# Description:
# ****************************************************************
import logging
import traceback
from django.core.exceptions import ValidationError as CoreValidationError
from rest_framework import status
from rest_framework.response import Response
from zibanu.django.auth.api.serializers import ProfileSerializer
from zibanu.django.auth.models import UserProfile
from zibanu.django.rest_framework.exceptions import ValidationError, APIException
from zibanu.django.rest_framework.viewsets import ModelViewSet
from zibanu.django.utils.error_messages import ErrorMessages
from zibanu.django.utils.user import get_user

class ProfileService(ModelViewSet):
    """
    Set of REST services for UserProfile model
    """
    model = UserProfile
    serializer_class = ProfileSerializer

    def update(self, request, *args, **kwargs) -> Response:
        """
        REST service to update UserProfile model

        Parameters
        ----------
        request: Request object from HTTP
        *args: Tuple of parameters
        **kwargs: Dictionary of parameters

        Returns
        -------
        response: Response object with HTTP status. 200 if success.
        """
        try:
            if request.data is not None:
                user = get_user(request.user)
                if hasattr(user, "profile"):
                    user.profile.set(fields=request.data)
                else:
                    raise ValidationError(ErrorMessages.NOT_FOUND, "user_profile_not_found")
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND, "data_request_error")
        except ValidationError as exc:
            raise APIException(msg=exc.detail[0], error=exc.detail[0].code, http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except CoreValidationError as exc:
            raise APIException(msg=exc.message, error=exc.code, http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            logging.error(str(exc))
            logging.debug(traceback.format_exc())
            raise APIException(msg=str(exc), error="not_controlled_exception", http_status=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
        else:
            return Response(status=status.HTTP_200_OK)

