from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Club
from .forms import ClubForm
from users.views import RoleRequiredMixin, UserRoleMixin


class ClubListView(ListView):
    model = Club
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'
    
    def get_queryset(self):
        return Club.objects.filter(is_approved=True)


class ClubDetailView(DetailView):
    model = Club
    template_name = 'clubs/club_detail.html'
    context_object_name = 'club'
    
    def get_queryset(self):
        return Club.objects.filter(is_approved=True)


class ClubCreateView(LoginRequiredMixin, UserRoleMixin, CreateView):
    model = Club
    form_class = ClubForm
    template_name = 'clubs/club_form.html'
    success_url = reverse_lazy('manager-dashboard')
    required_roles = ['club_manager', 'admin']
    
    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)


class ClubManagerDashboardView(LoginRequiredMixin, UserRoleMixin, ListView):
    model = Club
    template_name = 'clubs/manager_dashboard.html'
    context_object_name = 'my_clubs'
    required_roles = ['club_manager', 'admin']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Club.objects.all().prefetch_related('events')
        return Club.objects.filter(manager=self.request.user).prefetch_related('events')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from events.models import Event
        if self.request.user.role == 'admin':
            context['events'] = Event.objects.all().select_related('club')
        else:
            context['events'] = Event.objects.filter(club__manager=self.request.user).select_related('club')
        return context


class ClubUpdateView(LoginRequiredMixin, UserRoleMixin, UpdateView):
    model = Club
    form_class = ClubForm
    template_name = 'clubs/club_form.html'
    success_url = reverse_lazy('manager-dashboard')
    required_roles = ['club_manager', 'admin']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Club.objects.all()
        return Club.objects.filter(manager=self.request.user)
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user.role == 'admin':
            return True
        return obj.manager == self.request.user


class ClubDeleteView(LoginRequiredMixin, UserRoleMixin, DeleteView):
    model = Club
    template_name = 'clubs/club_confirm_delete.html'
    success_url = reverse_lazy('manager-dashboard')
    required_roles = ['club_manager', 'admin']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Club.objects.all()
        return Club.objects.filter(manager=self.request.user)
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user.role == 'admin':
            return True
        return obj.manager == self.request.user


class JoinClubView(LoginRequiredMixin, UserRoleMixin, View):
    required_roles = ['student', 'club_manager']
    
    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(Club, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if request.user.role == 'club_manager' and self.club.manager == request.user:
            messages.warning(request, 'You cannot join your own club.')
            return redirect('club-list')
        if request.user in self.club.members.all():
            messages.warning(request, 'You are already a member of this club.')
            return redirect('club-list')
        return render(request, 'clubs/join_confirmation.html', {'object': self.club})
    
    def post(self, request, *args, **kwargs):
        if request.user.role == 'club_manager' and self.club.manager == request.user:
            messages.warning(request, 'You cannot join your own club.')
            return redirect('club-list')
        if request.user in self.club.members.all():
            messages.warning(request, 'You are already a member of this club.')
            return redirect('club-list')
        self.club.members.add(request.user)
        messages.success(request, f'Successfully joined "{self.club.name}".')
        return redirect('club-list')


class LeaveClubView(LoginRequiredMixin, UserRoleMixin, View):
    required_roles = ['student', 'club_manager']
    
    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(Club, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if request.user not in self.club.members.all():
            messages.warning(request, 'You are not a member of this club.')
            return redirect('profile')
        return render(request, 'clubs/leave_confirmation.html', {'object': self.club})
    
    def post(self, request, *args, **kwargs):
        if request.user not in self.club.members.all():
            messages.warning(request, 'You are not a member of this club.')
            return redirect('profile')
        self.club.members.remove(request.user)
        messages.success(request, f'Successfully left "{self.club.name}".')
        return redirect('profile')


class AdminClubListView(LoginRequiredMixin, UserRoleMixin, ListView):
    model = Club
    template_name = 'clubs/admin_club_list.html'
    context_object_name = 'clubs'
    required_roles = ['admin']
    
    def get_queryset(self):
        return Club.objects.all()


class AdminClubDeleteView(LoginRequiredMixin, UserRoleMixin, DeleteView):
    model = Club
    template_name = 'clubs/admin_club_confirm_delete.html'
    success_url = reverse_lazy('admin-club-list')
    required_roles = ['admin']
    
    def get_queryset(self):
        return Club.objects.all()


class AdminClubRejectView(LoginRequiredMixin, UserRoleMixin, UpdateView):
    model = Club
    template_name = 'clubs/admin_club_confirm_reject.html'
    fields = []
    success_url = reverse_lazy('admin-club-list')
    required_roles = ['admin']
    
    def get_queryset(self):
        return Club.objects.all()
    
    def form_valid(self, form):
        self.object.is_approved = False
        self.object.save()
        return super().form_valid(form)