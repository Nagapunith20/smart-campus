
import uuid

from django.db import models
from django.conf import settings
from departments.models import Department


class Event(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    EVENT_TYPE_CHOICES = [
        ('free', 'Free Event'),
        ('paid', 'Paid Event'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='events'
    )

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )

    venue = models.CharField(max_length=200)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    event_type = models.CharField(
        max_length=10,
        choices=EVENT_TYPE_CHOICES,
        default='free'
    )

    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    max_participants = models.PositiveIntegerField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['event_date', 'start_time']


# EVENT REGISTRATION MODEL

class EventRegistration(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('not_required', 'Not Required'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    # DIGITAL TICKET FIELDS

    ticket_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    ticket_generated = models.BooleanField(default=False)

    attended = models.BooleanField(default=False)

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'event')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.student.username} - {self.event.title}"
