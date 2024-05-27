from django.core.management.base import BaseCommand
from todo_api.models import Tenant, Subscription, Subscriber

class Command(BaseCommand):
    help = 'Update plan from A to D'

    def handle(self, *args, **kwargs):

        old_plan = 'D' #changed
        new_plan = 'A' #changed
        
        subscription = Subscription.objects.filter(plan=old_plan).first()
        if subscription:
            subscription.plan = new_plan
            subscription.save()
            self.stdout.write(self.style.SUCCESS(f'Updated Subscription plan from {old_plan} to {new_plan}'))

        Tenant.objects.filter(plan_subscription=old_plan).update(plan_subscription=new_plan)
        self.stdout.write(self.style.SUCCESS(f'Updated Tenant entries from {old_plan} to {new_plan}'))

        Subscriber.objects.filter(plan__plan=old_plan).update(plan=new_plan)
        self.stdout.write(self.style.SUCCESS(f'Updated Subscriber entries from {old_plan} to {new_plan}'))

        deleted_count, _ = Subscription.objects.filter(plan=old_plan).delete()
        self.stdout.write(self.style.SUCCESS(f'Plan {old_plan} has been deleted'))

        self.stdout.write(self.style.SUCCESS('Successfully updated plan subscriptions'))



