from django.views.generic import ListView
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = "events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all().order_by('event_date')