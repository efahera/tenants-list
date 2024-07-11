# todo_api/management/commands/update_temporary.py

'''
STEP 2

update_temporary.py is to:
1. write data from subscriber --> temporary.csv
2. clear temporary table
3. reads csv file and write to temporary database table  

To run this command:
python manage.py update_temporary

'''

import csv
from django.core.management.base import BaseCommand
from django.db import connection
from todo_api.models import Temporary, Tenant, Subscription, Subscriber

class Command(BaseCommand):
    help = 'Populate the Temporary table with data from Tenant, Subscription, and Subscriber tables'

    def handle(self, *args, **kwargs):
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
