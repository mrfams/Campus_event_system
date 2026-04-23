from django.urls import path
from .views import EventPageView

urlpatterns = [
    path('', EventPageView.as_view(), name='event'),
]