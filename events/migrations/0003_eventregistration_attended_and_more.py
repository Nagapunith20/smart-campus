
import uuid

from django.db import migrations, models


def generate_ticket_ids(apps, schema_editor):
    EventRegistration = apps.get_model(
        'events',
        'EventRegistration'
    )

    database = schema_editor.connection.alias

    registrations = EventRegistration.objects.using(database).filter(
        ticket_id__isnull=True
    )

    for registration in registrations.iterator():
        registration.ticket_id = uuid.uuid4()
        registration.save(
            using=database,
            update_fields=['ticket_id']
        )


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_eventregistration'),
    ]

    operations = [

        # These columns already exist in MySQL.
        # Update Django's migration state without adding them again.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='eventregistration',
                    name='attended',
                    field=models.BooleanField(default=False),
                ),
                migrations.AddField(
                    model_name='eventregistration',
                    name='ticket_generated',
                    field=models.BooleanField(default=False),
                ),
            ],
        ),

        # First add Ticket ID as nullable.
        migrations.AddField(
            model_name='eventregistration',
            name='ticket_id',
            field=models.UUIDField(
                null=True,
                editable=False,
            ),
        ),

        # Generate a different UUID for every existing registration.
        migrations.RunPython(
            generate_ticket_ids,
            migrations.RunPython.noop,
        ),

        # Now make Ticket ID unique and required.
        migrations.AlterField(
            model_name='eventregistration',
            name='ticket_id',
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
            ),
        ),
    ]
