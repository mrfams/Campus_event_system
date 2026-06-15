from django.urls import path
from .views import ClubListView, ClubCreateView, ClubManagerDashboardView, ClubUpdateView, ClubDeleteView, ClubDetailView, JoinClubView, LeaveClubView, AdminClubListView, AdminClubDeleteView, AdminClubRejectView

urlpatterns = [
    path('', ClubListView.as_view(), name='club-list'),
    path('<int:pk>/', ClubDetailView.as_view(), name='club-detail'),
    path('create/', ClubCreateView.as_view(), name='club-create'),
    path('dashboard/', ClubManagerDashboardView.as_view(), name='manager-dashboard'),
    path('<int:pk>/edit/', ClubUpdateView.as_view(), name='club-edit'),
    path('<int:pk>/delete/', ClubDeleteView.as_view(), name='club-delete'),
    path('<int:pk>/join/', JoinClubView.as_view(), name='club-join'),
    path('<int:pk>/leave/', LeaveClubView.as_view(), name='club-leave'),
    path('admin/', AdminClubListView.as_view(), name='admin-club-list'),
    path('admin/<int:pk>/delete/', AdminClubDeleteView.as_view(), name='admin-club-delete'),
    path('admin/<int:pk>/reject/', AdminClubRejectView.as_view(), name='admin-club-reject'),
]