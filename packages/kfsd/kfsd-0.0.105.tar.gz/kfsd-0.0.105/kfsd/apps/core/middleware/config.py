from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig


class KubefacetsConfigMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.__config = self.genConfig()

    def genConfig(self):
        return KubefacetsConfig().getConfig()

    def __call__(self, request):
        request.config = self.__config
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None
