
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class StudentRegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser

        fields = [
            'username',
            'email',
            'student_id',
            'department',
            'year',
            'phone_number',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your college email'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your student ID'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'year': forms.Select(attrs={
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'

        if commit:
            user.save()

        return user


# STUDENT PROFILE FORM
class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'department',
            'year',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'year': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
