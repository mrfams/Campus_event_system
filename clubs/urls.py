from django.urls import path
from .views import ClubPageView

urlpatterns = [
    path('', ClubPageView.as_view(), name='club'),
]