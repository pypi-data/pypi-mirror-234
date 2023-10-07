from rest_framework.views import Response, exception_handler
from rest_framework import status
import json
import traceback
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.core.exceptions import ValidationError as CoreValidationError
from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def isStacktraceEnabled():
    config = KubefacetsConfig().getConfig()
    return DictUtils.get_by_path(config, "services.features_enabled.stacktrace")


def KubefacetsAPIExceptionHandler(ex, context):
    response = exception_handler(ex, context)
    request = context["request"]
    errorData = {
        "status": "ERROR",
        "path": request.path,
        "method": request.method,
        "content_type": request.content_type,
        "query_params": request.query_params,
        "body": request.data,
        "cookies": request.COOKIES,
        "error": ex.__str__(),
    }
    try:
        errorJson = json.dumps(errorData, indent=4)
        logger.error(errorJson)
    except Exception:
        logger.error("Error: {}".format(errorData))

    # print error to console
    if isStacktraceEnabled():
        print("[[ STACKTRACE ]]")
        traceback.print_exc()

    if isinstance(ex, IntegrityError) and not response:
        response = Response(
            {"detail": ex.__str__(), "code": "bad_request"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(ex, TypeError) and not response:
        response = Response(
            {"detail": ex.__str__(), "code": "system_error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(ex, ValidationError):
        response = Response(
            {"detail": ex.args[0], "code": "bad_request"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(ex, CoreValidationError):
        response = Response(
            {"detail": ex.args[0], "code": "bad_request"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(ex, KubefacetsAPIException):
        response = Response(
            {"detail": ex.detail, "code": ex.default_code}, status=ex.status_code
        )
    return response
