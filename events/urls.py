from django.urls import path
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView, RegisterForEventView, CancelEventRegistrationView, AdminEventListView, AdminEventUpdateView, AdminEventDeleteView, EventCommentCreateView, EventParticipantsListView

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('club/<int:club_pk>/create/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/register/', RegisterForEventView.as_view(), name='event-register'),
    path('<int:pk>/unregister/', CancelEventRegistrationView.as_view(), name='event-unregister'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='event-edit'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('<int:pk>/participants/', EventParticipantsListView.as_view(), name='event-participants'),
    path('admin/', AdminEventListView.as_view(), name='admin-event-list'),
    path('admin/<int:pk>/edit/', AdminEventUpdateView.as_view(), name='admin-event-edit'),
    path('admin/<int:pk>/delete/', AdminEventDeleteView.as_view(), name='admin-event-delete'),
    path('<int:pk>/comment/', EventCommentCreateView.as_view(), name='event-comment'),
]