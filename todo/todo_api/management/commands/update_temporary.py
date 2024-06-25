# todo_api/management/commands/update_temporary.py

'''
STEP 2

update_temporary.py is to clear temporary table and populates the latest data.

To run this command:
python manage.py update_temporary

'''

from django.core.management.base import BaseCommand
from django.db import connection
from todo_api.models import Temporary, Tenant, Subscription, Subscriber

class Command(BaseCommand):
    help = 'Populate the Temporary table with data from Tenant, Subscription, and Subscriber tables'

    def handle(self, *args, **kwargs):
        Temporary.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE todo_api_temporary_id_seq RESTART WITH 1")

        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            Temporary.objects.create(
                temp_tenant=subscriber.tenant,
                temp_plan=subscriber.plan,
                temp_subscriber=subscriber,
                temp_tenant_name=subscriber.tenant.name,
                temp_duration=subscriber.plan.duration,
                temp_start_date=subscriber.start_date,
                temp_end_date=subscriber.end_date,
                temp_price=subscriber.plan.price
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the Temporary table'))
