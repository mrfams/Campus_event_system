from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Event, EventRegistration, EventComment
from .forms import EventForm, EventCommentForm
from clubs.models import Club
from users.views import RoleRequiredMixin, UserRoleMixin


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        queryset = Event.objects.filter(club__is_approved=True, date__gte=timezone.now()).order_by('date')
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        return Event.objects.filter(club__is_approved=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_registered'] = self.object.registrations.filter(user=self.request.user).exists()
        else:
            context['user_registered'] = False
        return context


class EventCreateView(LoginRequiredMixin, UserRoleMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    required_roles = ['club_manager', 'admin']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['club'] = Club.objects.get(pk=self.kwargs['club_pk'])
        return kwargs

    def form_valid(self, form):
        form.instance.club_id = self.kwargs['club_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('manager-dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.club = Club.objects.get(pk=self.kwargs['club_pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def test_func(self):
        return self.club.manager == self.request.user


class EventUpdateView(LoginRequiredMixin, UserRoleMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    required_roles = ['club_manager', 'admin']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Event.objects.all()
        return Event.objects.filter(club__manager=self.request.user)
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user.role == 'admin':
            return True
        return obj.club.manager == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('manager-dashboard')


class EventDeleteView(LoginRequiredMixin, UserRoleMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    required_roles = ['club_manager', 'admin']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Event.objects.all()
        return Event.objects.filter(club__manager=self.request.user)
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user.role == 'admin':
            return True
        return obj.club.manager == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('manager-dashboard')


class RegisterForEventView(LoginRequiredMixin, UserRoleMixin, View):
    required_roles = ['student', 'club_manager']
    
    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # Prevent club manager from registering for their own event
        if request.user.role == 'club_manager' and self.event.club.manager == request.user:
            messages.warning(request, 'You cannot register for your own event.')
            return redirect('event-list')
        if EventRegistration.objects.filter(user=request.user, event=self.event).exists():
            messages.warning(request, 'You are already registered for this event.')
            return redirect('event-list')
        if self.event.registrations.count() >= self.event.max_participants:
            messages.warning(request, 'Event is full.')
            return redirect('event-list')
        EventRegistration.objects.create(user=request.user, event=self.event)
        messages.success(request, f'Successfully registered for "{self.event.title}".')
        return redirect('event-list')
    
    def post(self, request, *args, **kwargs):
        # Prevent club manager from registering for their own event
        if request.user.role == 'club_manager' and self.event.club.manager == request.user:
            messages.warning(request, 'You cannot register for your own event.')
            return redirect('event-list')
        if EventRegistration.objects.filter(user=request.user, event=self.event).exists():
            messages.warning(request, 'You are already registered for this event.')
            return redirect('event-list')
        if self.event.registrations.count() >= self.event.max_participants:
            messages.warning(request, 'Event is full.')
            return redirect('event-list')
        EventRegistration.objects.create(user=request.user, event=self.event)
        messages.success(request, f'Successfully registered for "{self.event.title}".')
        return redirect('event-list')


class CancelEventRegistrationView(LoginRequiredMixin, UserRoleMixin, View):
    required_roles = ['student']
    
    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=self.kwargs['pk'])
        self.registration = get_object_or_404(EventRegistration, event=self.event, user=request.user)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, 'events/unregister_confirmation.html', {'object': self.registration})
    
    def post(self, request, *args, **kwargs):
        event_title = self.registration.event.title
        self.registration.delete()
        messages.success(request, f'Registration cancelled for "{event_title}".')
        return redirect('event-list')


class EventCommentCreateView(LoginRequiredMixin, UserRoleMixin, CreateView):
    model = EventComment
    form_class = EventCommentForm
    template_name = 'events/comment_form.html'
    required_roles = ['student']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('event-detail', kwargs={'pk': self.kwargs['pk']})


class AdminEventListView(LoginRequiredMixin, UserRoleMixin, ListView):
    model = Event
    template_name = 'events/admin_event_list.html'
    context_object_name = 'events'
    required_roles = ['admin']
    
    def get_queryset(self):
        return Event.objects.all().order_by('-date')


class AdminEventUpdateView(LoginRequiredMixin, UserRoleMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    required_roles = ['admin']
    
    def get_queryset(self):
        return Event.objects.all()
    
    def get_success_url(self):
        return reverse_lazy('admin-event-list')


class AdminEventDeleteView(LoginRequiredMixin, UserRoleMixin, DeleteView):
    model = Event
    template_name = 'events/admin_event_confirm_delete.html'
    required_roles = ['admin']
    
    def get_queryset(self):
        return Event.objects.all()
    
    def get_success_url(self):
        return reverse_lazy('admin-event-list')


class EventParticipantsListView(LoginRequiredMixin, UserRoleMixin, ListView):
    model = EventRegistration
    template_name = 'events/event_participants.html'
    context_object_name = 'registrations'
    required_roles = ['club_manager', 'admin']
    
    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return EventRegistration.objects.filter(event=self.event).select_related('user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        context['registrations'] = self.get_queryset()
        return context
    
    def test_func(self):
        if self.request.user.role == 'admin':
            return True
        return self.event.club.manager == self.request.user