# todo_api/management/commands/populate_all.py

'''
STEP 3

populate_all.py is to populate all latest data from temporary table.

To run this command:
python manage.py populate_all

'''

from django.core.management.base import BaseCommand
from todo_api.models import Temporary, Tenant, Subscriber, Subscription

class Command(BaseCommand):
    help = 'Update the Tenant, Subscriber, and Subscription tables with data from the Temporary table'

    def handle(self, *args, **kwargs):
        self.populate_tenant()
        self.populate_subscriber()
        self.populate_subscription()

    def populate_tenant(self):
        temp_records = Temporary.objects.all().order_by('id')
        processed_ids = set()

        for temp in temp_records:
            if temp.temp_tenant_id in processed_ids:
                self.stdout.write(self.style.WARNING(f'Tenant ID {temp.temp_tenant_id} is duplicated. Record ignored'))
                continue

            tenant = Tenant.objects.filter(id=temp.temp_tenant_id).first()
            if tenant:
                tenant.name = temp.temp_tenant_name
                tenant.save()
                self.stdout.write(self.style.SUCCESS(f'Updated tenant with ID {temp.temp_tenant_id}'))

            else:
                self.stdout.write(self.style.WARNING(f'Tenant with ID {temp.temp_tenant_id} does not exist.'))

            processed_ids.add(temp.temp_tenant_id)

        self.stdout.write(self.style.SUCCESS('Successfully updated the Tenant table'))

    def populate_subscriber(self):
        temp_records = Temporary.objects.all().order_by('id')
        processed_ids = set()

        for temp in temp_records:
            if temp.temp_subscriber_id in processed_ids:
                self.stdout.write(self.style.WARNING(f'Subscriber ID {temp.temp_subscriber_id} is duplicated. Record ignored'))
                continue

            try:
                subscriber = Subscriber.objects.get(id=temp.temp_subscriber_id)
                subscriber.start_date = temp.temp_start_date
                subscriber.end_date = temp.temp_end_date
                subscriber.save()
                self.stdout.write(self.style.SUCCESS(f'Updated subscriber with ID {temp.temp_subscriber_id}'))

            except Subscriber.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Subscriber with ID {temp.temp_subscriber_id} does not exist.'))

            processed_ids.add(temp.temp_subscriber_id)
                
        self.stdout.write(self.style.SUCCESS('Successfully populated the Subscriber table'))

    def populate_subscription(self):
        temp_records = Temporary.objects.all().order_by('id')
        processed_ids = set()

        for temp in temp_records:
            if temp.temp_plan_id in processed_ids:
                self.stdout.write(self.style.WARNING(f'Subscription ID {temp.temp_plan_id} is duplicated. Record ignored'))
                continue

            try:
                subscription = Subscription.objects.get(plan=temp.temp_plan_id)
                subscription.duration = temp.temp_duration
                subscription.price = temp.temp_price
                subscription.save()
                self.stdout.write(self.style.SUCCESS(f'Updated subscription with Plan {temp.temp_plan_id}'))
                
            except Subscription.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Plan {temp.temp_plan_id} does not exist.'))

            processed_ids.add(temp.temp_plan_id)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Subscription table'))
