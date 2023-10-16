from kfsd.apps.core.auth.token import TokenUser
from kfsd.apps.core.utils.http.django.response import DjangoResponse


class KubefacetsTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        request.token_user = TokenUser(request)
        response = self.get_response(request)
        return self.processResponse(response, request)

    def processResponse(self, response, request):
        cookies = request.token_user.getUserCookies()
        djangoResponse = DjangoResponse(response)
        if cookies:
            for cookie in cookies:
                djangoResponse.setCookie(**cookie)
        return djangoResponse.getResponse()
