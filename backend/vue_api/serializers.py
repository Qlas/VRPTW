from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from .models import Client, ClientDistance, Result, ResultClient


class ClientSerializer(serializers.ModelSerializer):
    cost = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    def get_cost(self, obj):
        cost = {}
        for client1 in obj.client1.all():
            cost[client1.client2.name] = client1.cost
        for client2 in obj.client2.all():
            cost[client2.client1.name] = client2.cost
        return cost

    def get_time(self, obj):
        time = {}
        for client1 in obj.client1.all():
            time[client1.client2.name] = client1.time
        for client2 in obj.client2.all():
            time[client2.client1.name] = client2.time
        return time

    class Meta:
        model = Client
        fields = "__all__"


class ClientDistanceSerializer(serializers.ModelSerializer):
    client1 = serializers.SlugRelatedField(slug_field="name", queryset=Client.objects.all())
    client2 = serializers.SlugRelatedField(slug_field="name", queryset=Client.objects.all())

    class Meta:
        model = ClientDistance
        fields = "__all__"


class ResultClientSerializer(serializers.ModelSerializer):
    result = serializers.SlugRelatedField(slug_field="name", queryset=Result.objects.all())
    client = serializers.SlugRelatedField(slug_field="name", queryset=Client.objects.all())

    class Meta:
        model = ResultClient
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    result_client = ResultClientSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Result
        fields = "__all__"
