from django import forms
from .models import Club


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "description", "logo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["logo"].required = True

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and len(name) < 2:
            raise forms.ValidationError("Club name must be at least 2 characters.")
        return name
