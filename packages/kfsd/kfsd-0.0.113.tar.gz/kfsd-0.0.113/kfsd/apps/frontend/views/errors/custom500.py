from django.views.generic import TemplateView


class Custom500View(TemplateView):
    template_name = "v1/errors/500.html"
    status = 500
