from django.views.generic import TemplateView
from events.models import Event
from clubs.models import Club

class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['events'] = Event.objects.all().order_by('event_date')
        context['clubs'] = Club.objects.filter(is_approved=True)

        return context