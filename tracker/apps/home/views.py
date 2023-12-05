from django.views.generic import TemplateView


class FrontPageView(TemplateView):
    template_name = "home/frontpage.html"
