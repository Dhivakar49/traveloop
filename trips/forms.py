from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Trip, Stop, ChecklistItem, TripNote, UserProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name', 'description', 'start_date', 'end_date', 'cover_photo', 'budget', 'is_public']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'budget': forms.NumberInput(attrs={'class': 'form-input'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        if start and end and end < start:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned


class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        fields = ['city', 'arrival_date', 'departure_date', 'accommodation_cost',
                  'transport_cost', 'meal_cost_per_day', 'notes']
        widgets = {
            'arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'departure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'accommodation_cost': forms.NumberInput(attrs={'class': 'form-input'}),
            'transport_cost': forms.NumberInput(attrs={'class': 'form-input'}),
            'meal_cost_per_day': forms.NumberInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }


class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Item name...'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
        }


class TripNoteForm(forms.ModelForm):
    class Meta:
        model = TripNote
        fields = ['title', 'content', 'stop']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'stop': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, trip, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stop'].queryset = trip.stops.all()
        self.fields['stop'].required = False


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ['photo', 'language']
        widgets = {
            'language': forms.Select(
                choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('de', 'German')],
                attrs={'class': 'form-input'}
            ),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-input'

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save()
            profile.save()
        return profile
