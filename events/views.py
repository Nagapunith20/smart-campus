
import uuid
import qrcode

from io import BytesIO
from base64 import b64encode

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

from .forms import EventCreationForm, EventRegistrationForm
from .models import Event, EventRegistration


# FACULTY EVENT CREATION

@login_required
def create_event(request):

    if request.user.role != 'faculty':
        raise PermissionDenied

    if request.method == 'POST':
        form = EventCreationForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.status = 'pending'
            event.save()

            messages.success(
                request,
                'Event submitted successfully for admin approval!'
            )

            return redirect('create_event')

    else:
        form = EventCreationForm()

    return render(
        request,
        'events/create_event.html',
        {'form': form}
    )


# STUDENT EVENT DETAILS PAGE

@login_required
def event_detail(request, event_id):

    if request.user.role != 'student':
        raise PermissionDenied

    event = get_object_or_404(
        Event.objects.select_related('department', 'organizer'),
        id=event_id,
        status='approved'
    )

    registered_count = EventRegistration.objects.filter(
        event=event,
        payment_status__in=['paid', 'not_required']
    ).count()

    available_seats = max(
        event.max_participants - registered_count,
        0
    )

    return render(
        request,
        'events/event_detail.html',
        {
            'event': event,
            'registered_count': registered_count,
            'available_seats': available_seats,
        }
    )


# STUDENT EVENT REGISTRATION FORM

@login_required
def register_event(request, event_id):

    if request.user.role != 'student':
        raise PermissionDenied

    event = get_object_or_404(
        Event,
        id=event_id,
        status='approved'
    )

    if EventRegistration.objects.filter(
        student=request.user,
        event=event
    ).exists():

        messages.warning(
            request,
            'You have already registered for this event.'
        )

        return redirect('event_detail', event_id=event.id)

    # PAID EVENT HANDLING

    if event.event_type == 'paid':
        messages.info(
            request,
            'Online payment registration will be available soon.'
        )

        return redirect('event_detail', event_id=event.id)

    initial_data = {
        'full_name': request.user.get_full_name(),
        'email': request.user.email,
        'student_id': request.user.student_id,
        'department': (
            request.user.department.name
            if request.user.department else ''
        ),
        'year': request.user.year,
        'phone_number': request.user.phone_number,
    }

    if request.method == 'POST':

        form = EventRegistrationForm(
            request.POST,
            initial=initial_data
        )

        if form.is_valid():

            with transaction.atomic():

                existing_registration = EventRegistration.objects.filter(
                    student=request.user,
                    event=event
                ).exists()

                if existing_registration:
                    messages.warning(
                        request,
                        'You have already registered for this event.'
                    )

                    return redirect(
                        'event_detail',
                        event_id=event.id
                    )

                registered_count = EventRegistration.objects.filter(
                    event=event,
                    payment_status__in=['paid', 'not_required']
                ).count()

                if registered_count >= event.max_participants:

                    messages.error(
                        request,
                        'Sorry! This event is full.'
                    )

                    return redirect(
                        'event_detail',
                        event_id=event.id
                    )

                name_parts = form.cleaned_data['full_name'].strip().split(
                    maxsplit=1
                )

                request.user.first_name = name_parts[0]
                request.user.last_name = (
                    name_parts[1] if len(name_parts) > 1 else ''
                )

                request.user.email = form.cleaned_data['email']
                request.user.student_id = form.cleaned_data['student_id']
                request.user.phone_number = form.cleaned_data['phone_number']

                request.user.save()

                EventRegistration.objects.create(
                    student=request.user,
                    event=event,
                    payment_status='not_required'
                )

            return render(
                request,
                'events/registration_success.html',
                {'event': event}
            )

    else:
        form = EventRegistrationForm(initial=initial_data)

    return render(
        request,
        'events/registration_form.html',
        {
            'event': event,
            'form': form,
        }
    )


# STUDENT MY REGISTRATIONS PAGE

@login_required
def my_registrations(request):

    if request.user.role != 'student':
        raise PermissionDenied

    registrations = EventRegistration.objects.filter(
        student=request.user
    ).select_related(
        'event',
        'event__department'
    ).order_by('-registered_at')

    return render(
        request,
        'events/my_registrations.html',
        {
            'registrations': registrations,
        }
    )


# GENERATE QR CODE

def generate_ticket_qr(ticket_id):

    qr_data = f"SMART-CAMPUS-TICKET:{ticket_id}"

    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format='PNG')

    return buffer.getvalue()


# STUDENT DIGITAL TICKET PAGE

@login_required
def digital_ticket(request, ticket_id):

    if request.user.role != 'student':
        raise PermissionDenied

    registration = get_object_or_404(
        EventRegistration.objects.select_related(
            'student',
            'event',
            'event__department'
        ),
        ticket_id=ticket_id,
        student=request.user
    )

    # Do not issue tickets for unpaid paid events.

    if (
        registration.event.event_type == 'paid'
        and registration.payment_status != 'paid'
    ):
        messages.warning(
            request,
            'Your ticket will be available after successful payment.'
        )
        return redirect('my_registrations')

    registration.ticket_generated = True
    registration.save(update_fields=['ticket_generated'])

    qr_image = generate_ticket_qr(registration.ticket_id)

    qr_base64 = b64encode(qr_image).decode('utf-8')

    return render(
        request,
        'events/digital_ticket.html',
        {
            'registration': registration,
            'qr_code': qr_base64,
        }
    )


# DOWNLOAD DIGITAL TICKET AS PDF

@login_required
def download_ticket_pdf(request, ticket_id):

    if request.user.role != 'student':
        raise PermissionDenied

    registration = get_object_or_404(
        EventRegistration.objects.select_related(
            'student',
            'event',
            'event__department'
        ),
        ticket_id=ticket_id,
        student=request.user
    )

    if (
        registration.event.event_type == 'paid'
        and registration.payment_status != 'paid'
    ):
        messages.warning(
            request,
            'Your ticket will be available after successful payment.'
        )
        return redirect('my_registrations')

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    event = registration.event
    student = registration.student

    pdf.setTitle('SMART CAMPUS Digital Ticket')

    pdf.setFont('Helvetica-Bold', 22)
    pdf.drawCentredString(
        width / 2,
        height - 70,
        'SMART CAMPUS'
    )

    pdf.setFont('Helvetica-Bold', 17)
    pdf.drawCentredString(
        width / 2,
        height - 110,
        'EVENT ADMISSION TICKET'
    )

    pdf.setFont('Helvetica', 12)

    details = [
        f"Ticket ID: {registration.ticket_id}",
        f"Student Name: {student.get_full_name()}",
        f"Student ID: {student.student_id or 'Not provided'}",
        f"Email: {student.email}",
        f"Event: {event.title}",
        f"Department: {event.department.name}",
        f"Date: {event.event_date}",
        f"Time: {event.start_time} - {event.end_time}",
        f"Venue: {event.venue}",
        f"Payment Status: {registration.get_payment_status_display()}",
    ]

    y = height - 165

    for detail in details:
        pdf.drawString(65, y, detail)
        y -= 28

    qr_image = generate_ticket_qr(registration.ticket_id)

    qr_buffer = BytesIO(qr_image)

    pdf.drawImage(
        ImageReader(qr_buffer),
        width / 2 - 65,
        y - 155,
        width=130,
        height=130
    )

    pdf.setFont('Helvetica-Bold', 11)

    pdf.drawCentredString(
        width / 2,
        y - 180,
        'Show this QR code at the event entrance.'
    )

    pdf.save()

    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="SMART_CAMPUS_Ticket_{registration.ticket_id}.pdf"'
    )

    return response
