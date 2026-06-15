from django import forms
from .models import Event, EventComment
from clubs.models import Club


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'max_participants']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.club = kwargs.pop('club', None)
        super().__init__(*args, **kwargs)
        if self.club:
            self.instance.club = self.club

    def clean_max_participants(self):
        max_participants = self.cleaned_data.get('max_participants')
        if max_participants and max_participants < 1:
            raise forms.ValidationError('Max participants must be at least 1.')
        return max_participants


class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['content']