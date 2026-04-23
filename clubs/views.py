from django.views.generic import ListView
from .models import Club

class ClubListView(ListView):
    model = Club
    template_name = "clubs.html"
    context_object_name = "clubs"

    def get_queryset(self):
        return Club.objects.filter(is_approved=True)