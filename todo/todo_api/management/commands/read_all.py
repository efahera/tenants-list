# todo_api/management/commands/read_temporary.py

'''
STEP 1

update_temporary.py is to clear temporary table and populates the latest data.

To run this command:
python manage.py read_all --tenant_csv=path/to/tenant.csv --subscription_csv=path/to/subscription.csv --subscriber_csv=path/to/subscriber.csv 

'''

from django.core.management.base import BaseCommand
from todo_api.models import Tenant, Subscriber, Subscription
import csv
from datetime import datetime
from django.db import connection

class Command(BaseCommand):
    help = 'Update Tenant, Subscriber, and Subscription tables from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--tenant_csv', type=str, help='The path to the Tenant CSV file to be processed')
        parser.add_argument('--subscription_csv', type=str, help='The path to the Subscription CSV file to be processed')
        parser.add_argument('--subscriber_csv', type=str, help='The path to the Subscriber CSV file to be processed')

    def handle(self, *args, **kwargs):
        if kwargs['tenant_csv']:
            self.read_tenant(kwargs['tenant_csv'])
        
        if kwargs['subscription_csv']:
            self.read_subscription(kwargs['subscription_csv'])

        if kwargs['subscriber_csv']:
            self.read_subscriber(kwargs['subscriber_csv'])
        
        self.stdout.write(self.style.SUCCESS('Successfully processed all CSV files'))

    def read_tenant(self, csv_file_path):
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

    def read_subscription(self, csv_file_path):
        with open(csv_file_path, 'r') as file: 
            reader = csv.DictReader(file)
            for row in reader:
                plan_id = row['plan']
                duration = row['duration']
                price = row['price']

                subscription, created = Subscription.objects.update_or_create(
                    plan=plan_id,
                    defaults={
                        'duration': duration, 
                        'price': price
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created subscription {plan_id}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated subscription {plan_id}'))

    def read_subscriber(self, csv_file_path):
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
