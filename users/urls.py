from django.urls import path
from .views import UserPageView

urlpatterns = [
    path('', UserPageView.as_view(), name='user'),
]