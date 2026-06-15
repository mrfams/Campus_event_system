from django.urls import path
from users.views import RegisterView, UserLoginView, UserLogoutView, AdminClubListView, ClubApproveView, ProfileView, ProfileUpdateView, AdminUserListView, UserRoleUpdateView, UserDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('admin/clubs/', AdminClubListView.as_view(), name='admin-club-list'),
    path('admin/clubs/<int:pk>/approve/', ClubApproveView.as_view(), name='club-approve'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/role/', UserRoleUpdateView.as_view(), name='user-role'),
    path('admin/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]