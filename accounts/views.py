
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from events.models import Event
from .forms import StudentRegistrationForm, StudentProfileForm


# STUDENT REGISTRATION
def register(request):

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Registration successful! Please log in.'
            )

            return redirect('login')

    else:
        form = StudentRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


# STUDENT AND FACULTY LOGIN
def student_login(request):

    if request.user.is_authenticated:
        return redirect_user(request.user)

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            if user.role == 'student':
                login(request, user)
                return redirect('dashboard')

            elif user.role == 'faculty':
                login(request, user)
                return redirect('create_event')

            elif user.role == 'admin' and user.is_staff:
                login(request, user)
                return redirect('admin:index')

            else:
                messages.error(
                    request,
                    'Your account does not have permission to log in.'
                )

        else:
            messages.error(
                request,
                'Invalid email or password.'
            )

    return render(request, 'accounts/login.html')


# ROLE-BASED REDIRECTION
def redirect_user(user):

    if user.role == 'student':
        return redirect('dashboard')

    elif user.role == 'faculty':
        return redirect('create_event')

    elif user.role == 'admin' and user.is_staff:
        return redirect('admin:index')

    return redirect('login')


# STUDENT DASHBOARD
@login_required
def dashboard(request):

    if request.user.role != 'student':
        raise PermissionDenied

    return render(
        request,
        'accounts/dashboard.html'
    )


# STUDENT PROFILE
@login_required
def student_profile(request):

    if request.user.role != 'student':
        raise PermissionDenied

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your profile has been updated successfully!'
            )

            return redirect('student_profile')

    else:
        form = StudentProfileForm(instance=request.user)

    return render(
        request,
        'accounts/profile.html',
        {'form': form}
    )


# LOGOUT
@login_required
def student_logout(request):

    logout(request)

    messages.success(
        request,
        'You have logged out successfully.'
    )

    return redirect('login')


# SMART CAMPUS HOMEPAGE
def home(request):

    events = Event.objects.filter(
        status='approved'
    ).select_related('department').order_by('event_date')[:6]

    return render(
        request,
        'accounts/home.html',
        {'events': events}
    )
