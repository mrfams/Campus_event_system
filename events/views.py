from django.views.generic import TemplateView

class EventPageView(TemplateView):
    template_name = "events.html"