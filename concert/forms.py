from django import forms
from .models import CustomUser, Event, Ticket
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class EventForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # HTML5 date input widget
        label='Event Date'
    )
    event_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),  # HTML5 time input widget
        label='Event Time'
    )

    class Meta:
        model = Event
        fields = ['event_name', 'event_date', 'event_time', 'event_location', 'event_description', 'event_poster']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'ticket_quantity']

    TICKET_CHOICES = [
        ('VIP', 'VIP'),
        ('Standard', 'Standard'),
    ]
    ticket_type = forms.ChoiceField(choices=TICKET_CHOICES)
    ticket_quantity = forms.IntegerField(min_value=1)