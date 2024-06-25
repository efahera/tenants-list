# todo_api/management/commands/update_all.py

'''
STEP 1

update_all.py is to read data from CSV file.

To run this command:
python manage.py update_all --tenant_csv=path/to/tenant.csv --subscriber_csv=path/to/subscriber.csv --subscription_csv=path/to/subscription.csv 

'''

from django.core.management.base import BaseCommand
from todo_api.models import Tenant, Subscriber, Subscription, Temporary
import csv
from datetime import datetime

class Command(BaseCommand):
    help = 'Update Tenant, Subscriber, Subscription, and Temporary tables from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--tenant_csv', type=str, help='The path to the Tenant CSV file to be processed')
        parser.add_argument('--subscriber_csv', type=str, help='The path to the Subscriber CSV file to be processed')
        parser.add_argument('--subscription_csv', type=str, help='The path to the Subscription CSV file to be processed')
        parser.add_argument('--temporary_csv', type=str, help='The path to the Temporary CSV file to be processed')

    def handle(self, *args, **kwargs):
        if kwargs['tenant_csv']:
            self.update_tenant(kwargs['tenant_csv'])
        
        if kwargs['subscriber_csv']:
            self.update_subscriber(kwargs['subscriber_csv'])
        
        if kwargs['subscription_csv']:
            self.update_subscription(kwargs['subscription_csv'])
        
        if kwargs['temporary_csv']:
            self.update_temporary(kwargs['temporary_csv'])

        self.stdout.write(self.style.SUCCESS('Successfully processed all CSV files'))

        # self.populate_tenant()
        # self.populate_subscriber()
        # self.populate_subscription()

    def update_tenant(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row['id']
                name = row['name']
                age = row['age']
                date_of_birth = row['date_of_birth']
                contact_number = row['contact_number']
                image = row['image']
                plan_subscription = row['plan_subscription']
                status = row['status']

                if date_of_birth:
                    date_of_birth = datetime.strptime(date_of_birth, '%d/%m/%Y').date()

                tenant, created = Tenant.objects.update_or_create(
                    id=id,
                    defaults={
                        'name': name,
                        'age': age,
                        'date_of_birth': date_of_birth,
                        'contact_number': contact_number,
                        'image': image,
                        'plan_subscription': plan_subscription,
                        'status': status
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created tenant {id}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated tenant {id}'))

    def update_subscriber(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row['id']
                plan_id = row['plan_id']
                tenant_id = row['tenant_id']
                start_date = row['start_date']
                end_date = row['end_date']

                if start_date:
                    start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%d/%m/%Y').date()

                try:
                    plan = Subscription.objects.get(plan=plan_id)
                except Subscription.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Plan with ID {plan_id} does not exist. Skipping subscriber {id}.'))
                    continue

                try:
                    tenant = Tenant.objects.get(id=tenant_id)
                except Tenant.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Tenant with ID {tenant_id} does not exist. Skipping subscriber {id}.'))
                    continue

                subscriber, created = Subscriber.objects.update_or_create(
                    id=id,
                    defaults={'plan': plan, 'tenant': tenant, 'start_date': start_date, 'end_date': end_date}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created subscriber {id}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated subscriber {id}'))

    def update_subscription(self, csv_file_path):
        with open(csv_file_path, 'r') as file: 
            reader = csv.DictReader(file)
            for row in reader:
                plan_id = row['plan']
                duration = row['duration']
                price = row['price']

                # Update if exists, create if not
                subscription, created = Subscription.objects.update_or_create(
                    plan=plan_id,
                    defaults={'duration': duration, 'price': price}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created subscription {plan_id}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated subscription {plan_id}'))

