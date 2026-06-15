from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth import get_user_model, login
from django.utils import timezone
from django.http import HttpResponseForbidden
from .forms import RegistrationForm, ProfileUpdateForm
from clubs.models import Club


class RoleRequiredMixin(AccessMixin):
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != self.required_role:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        return HttpResponseForbidden()


class UserRoleMixin(AccessMixin):
    required_roles = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in self.required_roles:
            return self.handle_no_permission()
        if not self.test_func():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def test_func(self):
        return True
    
    def handle_no_permission(self):
        return HttpResponseForbidden()


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from clubs.models import Club
        from events.models import Event
        context['clubs'] = Club.objects.filter(is_approved=True)[:6]
        context['events'] = Event.objects.filter(club__is_approved=True, date__gte=timezone.now()).order_by('date')[:6]
        return context

User = get_user_model()
class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Auto-login after registration
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    
    def form_valid(self, form):
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class AdminClubListView(RoleRequiredMixin, ListView):
    required_role = 'admin'
    model = Club
    template_name = 'users/admin/club_approval.html'
    context_object_name = 'clubs'
    
    def get_queryset(self):
        return Club.objects.filter(is_approved=False).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth import get_user_model
        from events.models import Event
        User = get_user_model()
        context['clubs_pending_count'] = Club.objects.filter(is_approved=False).count()
        context['total_users'] = User.objects.count()
        context['total_clubs'] = Club.objects.count()
        context['total_events'] = Event.objects.count()
        context['approved_clubs'] = Club.objects.filter(is_approved=True).count()
        return context


class ClubApproveView(RoleRequiredMixin, UpdateView):
    required_role = 'admin'
    model = Club
    fields = ['is_approved']
    template_name = 'users/admin/approve_form.html'
    success_url = reverse_lazy('admin-club-list')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user


class UserRoleUpdateView(RoleRequiredMixin, UpdateView):
    required_role = 'admin'
    model = User
    template_name = 'users/admin/user_role_form.html'
    fields = ['role']
    success_url = reverse_lazy('admin-user-list')


class AdminUserListView(RoleRequiredMixin, ListView):
    required_role = 'admin'
    model = User
    template_name = 'users/admin/user_list.html'
    context_object_name = 'users'


class UserDeleteView(RoleRequiredMixin, DeleteView):
    required_role = 'admin'
    model = User
    template_name = 'users/admin/user_confirm_delete.html'
    success_url = reverse_lazy('admin-user-list')