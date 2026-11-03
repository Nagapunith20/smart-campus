
from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'department',
        'organizer',
        'event_date',
        'event_type',
        'registration_fee',
        'status'
    )

    list_filter = (
        'department',
        'event_type',
        'status',
        'event_date'
    )

    search_fields = (
        'title',
        'venue',
        'description'
    )

    readonly_fields = ('created_at',)

    list_editable = ('status',)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'event',
        'payment_status',
        'registered_at'
    )

    list_filter = (
        'payment_status',
        'registered_at'
    )

    search_fields = (
        'student__username',
        'student__email',
        'event__title'
    )

    readonly_fields = ('registered_at',)
