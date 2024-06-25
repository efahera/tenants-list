from django.urls import path, include
from rest_framework import routers
from .views import TenantViewSet, SubscriberViewSet, SubscriptionViewSet, TemporaryViewSet

router = routers.DefaultRouter()
router.register(r'Tenant', TenantViewSet)
router.register(r'Subscribers', SubscriberViewSet)
router.register(r'Subscriptions', SubscriptionViewSet)
router.register(r'Temporary', TemporaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


