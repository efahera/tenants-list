# todo_api/management/commands/read_temporary.py

'''
read_temporary.py is to read data from CSV file temporary into database.

To run this command:
python manage.py read_temporary --temporary_csv=path/to/temporary.csv 

'''

from django.core.management.base import BaseCommand
from todo_api.models import Tenant, Subscriber, Subscription, Temporary
import csv
from datetime import datetime
from django.db import connection

class Command(BaseCommand):
    help = 'Read Temporary table from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--temporary_csv', type=str, help='The path to the Temporary CSV file to be processed')

    def handle(self, *args, **kwargs):
        Temporary.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE todo_api_temporary_id_seq RESTART WITH 1")
        
        if kwargs['temporary_csv']:
            self.read_temporary(kwargs['temporary_csv'])

        self.stdout.write(self.style.SUCCESS('Successfully processed temporary CSV file'))

    def read_temporary(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row['id']
                temp_plan_id = row['temp_plan_id']
                temp_subscriber_id = row['temp_subscriber_id']
                temp_tenant_id = row['temp_tenant_id']
                temp_duration = row['temp_duration']
                temp_end_date = row['temp_end_date']
                temp_price = row['temp_price']
                temp_start_date = row['temp_start_date']
                temp_tenant_name = row['temp_tenant_name']

                if temp_start_date:
                    temp_start_date = datetime.strptime(temp_start_date, '%d/%m/%Y').date()
                if temp_end_date:
                    temp_end_date = datetime.strptime(temp_end_date, '%d/%m/%Y').date()

                try:
                    tenant = Tenant.objects.get(id=temp_tenant_id)
                except Tenant.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Tenant with ID {temp_tenant_id} does not exist. Skipping temporary record {id}.'))
                    continue

                try:
                    plan = Subscription.objects.get(plan=temp_plan_id)
                except Subscription.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Plan with ID {temp_plan_id} does not exist. Skipping temporary record {id}.'))
                    continue

                try:
                    subscriber = Subscriber.objects.get(id=temp_subscriber_id)
                except Subscriber.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Subscriber with ID {temp_subscriber_id} does not exist. Skipping temporary record {id}.'))
                    continue

                Temporary.objects.create(
                    temp_tenant = tenant,
                    temp_plan = plan,
                    temp_subscriber = subscriber,
                    temp_tenant_name = temp_tenant_name,
                    temp_duration = temp_duration,
                    temp_start_date = temp_start_date,
                    temp_end_date = temp_end_date,
                    temp_price = temp_price
                )

                self.stdout.write(self.style.SUCCESS(f'Created temporary record with tenant {temp_tenant_id}'))


