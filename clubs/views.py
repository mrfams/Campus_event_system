from django.views.generic import TemplateView

class ClubPageView(TemplateView):
    template_name = "clubs.html"