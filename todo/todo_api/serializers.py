from rest_framework import serializers
from .models import Tenant, Subscriber, Subscription

class TenantSerializer(serializers.ModelSerializer):
    plan_subscription = serializers.CharField(read_only=True)

    class Meta:
        model = Tenant
        fields = ['id', 'name', 'age', 'date_of_birth', 'contact_number', 'image', 'plan_subscription'] 

class SubscriberSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    end_date = serializers.DateField(read_only=True)

    class Meta:
        model = Subscriber
        fields = ['id', 'tenant', 'tenant_name', 'plan', 'start_date', 'end_date']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


