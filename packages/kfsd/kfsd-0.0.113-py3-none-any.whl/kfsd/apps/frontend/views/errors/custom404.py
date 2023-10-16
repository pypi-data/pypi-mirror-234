from django.views.generic import TemplateView


class Custom404View(TemplateView):
    template_name = "v1/errors/404.html"
    status = 404
