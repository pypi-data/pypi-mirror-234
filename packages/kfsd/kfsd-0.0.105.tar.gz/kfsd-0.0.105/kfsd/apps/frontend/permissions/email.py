from kfsd.apps.frontend.permissions.base import BasePermission
from kfsd.apps.core.exceptions.fe import KubefacetsFEException
from http import HTTPStatus


class SignUpEmailVerified(BasePermission):
    def __init__(self, request):
        BasePermission.__init__(self, request)

    def __str__(self):
        return "Is email verified check"

    def is_valid(self):
        if self.getUser().isEmailVerified():
            return True
        return False

    def raise_exception(self):
        raise KubefacetsFEException(
            self.__str__(), HTTPStatus.TEMPORARY_REDIRECT, self.redirect_url()
        )

    def redirect_url(self):
        verifyEmailUrl = self.formatUrl(
            self.getDjangoRequest().findConfigs(
                ["services.sso_fe.host", "services.sso_fe.email_verify_uri"]
            )
        )
        verifyEmailUrl += "?next={}".format(
            self.genUrlEncode(self.getCurrentRequestUrl())
        )
        return verifyEmailUrl

    def redirect_url_neg(self):
        verifiedFinalUrl = self.formatUrl(
            self.getDjangoRequest().findConfigs(["services.default_signedin_url"])
        )
        return verifiedFinalUrl

    def raise_exception_neg(self):
        raise KubefacetsFEException(
            self.__str__(), HTTPStatus.TEMPORARY_REDIRECT, self.redirect_url_neg()
        )
