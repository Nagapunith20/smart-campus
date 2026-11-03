
from django.urls import path
from . import views

urlpatterns = [

    # Faculty creates events
    path(
        'create/',
        views.create_event,
        name='create_event'
    ),

    # Student views their registrations
    path(
        'my-registrations/',
        views.my_registrations,
        name='my_registrations'
    ),

    # Student views digital ticket
    path(
        'ticket/<uuid:ticket_id>/',
        views.digital_ticket,
        name='digital_ticket'
    ),

    # Student downloads ticket PDF
    path(
        'ticket/<uuid:ticket_id>/download/',
        views.download_ticket_pdf,
        name='download_ticket_pdf'
    ),

    # Student registration
    path(
        '<int:event_id>/register/',
        views.register_event,
        name='register_event'
    ),

    # Student views event details
    path(
        '<int:event_id>/',
        views.event_detail,
        name='event_detail'
    ),

]
