
from django import forms
from .models import Event


class EventCreationForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            'title',
            'description',
            'department',
            'venue',
            'event_date',
            'start_time',
            'end_time',
            'event_type',
            'registration_fee',
            'max_participants',
        ]

        widgets = {
            'event_date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time'
            }),
        }


class EventRegistrationForm(forms.Form):

    full_name = forms.CharField(
        max_length=150,
        label="Full Name"
    )

    email = forms.EmailField(
        label="College Email"
    )

    student_id = forms.CharField(
        max_length=30,
        label="Student ID"
    )

    department = forms.CharField(
        max_length=100,
        label="Department"
    )

    year = forms.ChoiceField(
        choices=[
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
        ],
        label="Year of Study"
    )

    phone_number = forms.CharField(
        max_length=15,
        label="Phone Number"
    )
