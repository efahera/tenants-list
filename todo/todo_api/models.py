from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta
from django.utils import timezone

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('Z', 'Z'),
    ]
    plan = models.CharField(max_length=1, choices= PLAN_CHOICES, primary_key=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.get_plan_display()

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='tenant_images/', null=True, blank=True)
    plan_subscription = models.CharField(max_length=1, null=True, blank=True)  
    status = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def update_status(self):
        subscriber = Subscriber.objects.filter(tenant=self).order_by('plan').first()
        if subscriber and subscriber.end_date:
            if subscriber.end_date >= date.today():
                self.status = 'Ongoing'
            else:
                self.status = 'Expired'
        else:
            self.status = 'Invalid'
        self.save()

class Subscriber(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    plan = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True, null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.plan.get_plan_display()}"

    def calculate_end_date(self):
        if self.plan.plan   == 'A': 
            return self.start_date + relativedelta(months=1)
        elif self.plan.plan == 'B':
            return self.start_date + relativedelta(months=6)
        elif self.plan.plan == 'C':
            return self.start_date + relativedelta(months=12)
        elif self.plan.plan == 'D':
            return self.start_date + relativedelta(months=24)
        elif self.plan.plan == 'Z':
            return self.start_date + relativedelta(days=1)

        return None

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = date.today()

        # save 'calculate_end_date' as 'end_date'
        self.end_date = self.calculate_end_date()
        # save 'get_plan_display' as 'tenant.plan_subscription'
        self.tenant.plan_subscription = self.plan.get_plan_display()
        
        super().save(*args, **kwargs)
        self.tenant.update_status()

class Temporary(models.Model):
    
    temp_tenant  = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    temp_plan = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    temp_subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    temp_tenant_name = models.CharField(max_length=100, blank=True, null=True)
    temp_duration = models.CharField(max_length=20, blank=True, null=True)
    temp_start_date = models.DateField(blank=True, null=True)
    temp_end_date = models.DateField(blank=True, null=True)
    temp_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Temporary: {self.temp_tenant.name} - {self.temp_plan.plan} - {self.temp_subscriber.id}"
