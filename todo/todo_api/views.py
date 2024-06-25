from rest_framework import viewsets, status 
from rest_framework.response import Response
from .models import Tenant, Subscriber, Subscription, Temporary
from .serializers import TenantSerializer, SubscriberSerializer, SubscriptionSerializer, TemporarySerializer
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all().order_by('id')
    serializer_class = TenantSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = Tenant.objects.all().order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TenantSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TenantSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            tenant = Tenant.objects.get(id=pk)
        except Tenant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TenantSerializer(tenant)
        return Response(serializer.data)

    def create(self, request):
        serializer = TenantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            tenant = Tenant.objects.get(id=pk)
        except Tenant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TenantSerializer(tenant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            tenant = Tenant.objects.get(id=pk)
        except Tenant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        tenant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubscriberViewSet(viewsets.ModelViewSet):

    queryset = Subscriber.objects.all().order_by('id')
    serializer_class = SubscriberSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = Subscriber.objects.all().order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriberSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SubscriberSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            subscriber = Subscriber.objects.get(id=pk)
        except Subscriber.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriberSerializer(subscriber)
        return Response(serializer.data)

    def create(self, request):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            subscriber = Subscriber.objects.get(id=pk)
        except Subscriber.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriberSerializer(subscriber, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            subscriber = Subscriber.objects.get(id=pk)
        except Subscriber.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        subscriber.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = Subscription.objects.all().order_by('plan')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            subscription = Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def create(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            subscription = Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriptionSerializer(subscription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            subscription = Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TemporaryViewSet(viewsets.ModelViewSet):
    queryset = Temporary.objects.all()
    serializer_class = TemporarySerializer

