from rest_framework import serializers
from .models import Tenant, Subscriber, Subscription, Temporary

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class TenantSerializer(serializers.ModelSerializer):
    plan_subscription = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Tenant
        fields = '__all__'

class SubscriberSerializer(serializers.ModelSerializer):

    # user input field
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all().order_by('id'), write_only=True)
    plan = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all().order_by('plan'), write_only=True)
    
    # retrieve from tenant and subscription table
    tenant_id = serializers.CharField(source='tenant.id', read_only=True)
    end_date = serializers.DateField(read_only=True)

    class Meta:
        model = Subscriber
        fields = ['id', 'tenant', 'tenant_id', 'plan_id', 'plan', 'start_date', 'end_date']


class TemporarySerializer(serializers.ModelSerializer):
    temp_tenant_name = serializers.CharField(source='temp_tenant.name', read_only=True)
    temp_duration = serializers.CharField(source='temp_plan.duration', read_only=True)
    temp_start_date = serializers.DateField(source='temp_subscriber.start_date', read_only=True)
    temp_end_date = serializers.DateField(source='temp_subscriber.end_date', read_only=True)
    temp_price = serializers.DecimalField(source='temp_plan.price', max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Temporary 
        fields = ['id', 'temp_tenant_name', 'temp_plan_id', 'temp_duration', 'temp_start_date', 'temp_end_date', 'temp_price']


