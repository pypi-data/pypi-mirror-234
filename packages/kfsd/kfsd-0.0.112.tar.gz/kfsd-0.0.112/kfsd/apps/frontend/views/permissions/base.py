from django.views.generic import View
from http import HTTPStatus
from django.http import (
    HttpResponseRedirect,
    HttpResponseNotFound,
    HttpResponseServerError,
    HttpResponseForbidden,
)

from kfsd.apps.core.exceptions.fe import KubefacetsFEException
from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class PermissionView(View):
    def verifyPermission(self, permission):
        if not permission.is_valid():
            permission.raise_exception()
        return True

    def verifyPermissionNeg(self, permission):
        if permission.is_valid():
            permission.raise_exception_neg()
        return True

    def getPermissionsClasses(self, argName):
        if hasattr(self, argName):
            return getattr(self, argName)
        return []

    def checkAllPermissions(self, request):
        for permission in self.getPermissionsClasses("permission_classes"):
            permissionObj = permission(request)
            self.verifyPermission(permissionObj)
        return True

    def checkAllPermissionsNeg(self, request):
        for permission in self.getPermissionsClasses("permission_classes_neg"):
            permissionObj = permission(request)
            self.verifyPermissionNeg(permissionObj)
        return True

    def isAuthEnabled(self):
        config = KubefacetsConfig().getConfig()
        isAuth = DictUtils.get_by_path(config, "services.features_enabled.auth")
        return isAuth if isAuth else False

    def dispatch(self, request, *args, **kwargs):
        try:
            if self.isAuthEnabled():
                self.checkAllPermissions(request)
                self.checkAllPermissionsNeg(request)
            return super().dispatch(request, *args, **kwargs)
        except KubefacetsFEException as ex:
            if ex.status_code == HTTPStatus.TEMPORARY_REDIRECT:
                return HttpResponseRedirect(ex.redirect_url)
            if ex.status_code == HTTPStatus.NOT_FOUND:
                return HttpResponseNotFound()
            if ex.status_code == HTTPStatus.FORBIDDEN:
                return HttpResponseForbidden()
            return HttpResponseServerError()
        except KubefacetsAPIException:
            return HttpResponseServerError()
