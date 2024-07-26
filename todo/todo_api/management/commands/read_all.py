# todo_api/management/commands/read_all.py

'''

read_all.py is to read Tenant, Subscriber, and Subscription CSV files and write to Temporary CSV file.

To run this command:
python manage.py read_all --tenant_csv=path/to/tenant.csv --subscription_csv=path/to/subscription.csv --subscriber_csv=path/to/subscriber.csv 

'''

from django.core.management.base import BaseCommand
from todo_api.models import Tenant, Subscriber, Subscription,Temporary
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

        self.update_temporary()

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

    def update_temporary(self):
        csv_file_path = 'temporary.csv'
        subscribers = Subscriber.objects.all()

        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = [
                'id',
                'temp_tenant_id', 
                'temp_tenant_name', 
                'temp_plan_id',
                'temp_duration', 
                'temp_price', 
                'temp_subscriber_id',
                'temp_start_date', 
                'temp_end_date'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            count_id = 1
            for subscriber in subscribers:
                writer.writerow({
                    'id': count_id,
                    'temp_tenant_id': subscriber.tenant.id,
                    'temp_tenant_name': subscriber.tenant.name,
                    'temp_plan_id': subscriber.plan.plan,
                    'temp_duration': subscriber.plan.duration,
                    'temp_price': subscriber.plan.price,
                    'temp_subscriber_id': subscriber.id,
                    'temp_start_date': subscriber.start_date.strftime('%Y-%m-%d'),
                    'temp_end_date': subscriber.end_date.strftime('%Y-%m-%d')
                })
                count_id += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully wrote data to {csv_file_path}'))

        Temporary.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE todo_api_temporary_id_seq RESTART WITH 1")

        temp_records = []
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_records.append(Temporary(
                    temp_tenant_id=row['temp_tenant_id'],
                    temp_tenant_name=row['temp_tenant_name'],
                    temp_plan_id=row['temp_plan_id'],
                    temp_duration=row['temp_duration'],
                    temp_price=row['temp_price'],
                    temp_subscriber_id=row['temp_subscriber_id'],
                    temp_start_date=row['temp_start_date'],
                    temp_end_date=row['temp_end_date']
                ))

        Temporary.objects.bulk_create(temp_records)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Temporary table from CSV file'))