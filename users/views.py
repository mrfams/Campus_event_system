from django.views.generic import ListView
from .models import User

class UserListView(ListView):
    model = User
    template_name = "users.html"
    context_object_name = "users"