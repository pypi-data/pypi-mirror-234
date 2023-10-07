from django.views.generic import TemplateView


class Custom403View(TemplateView):
    template_name = "v1/errors/403.html"
    status = 403
