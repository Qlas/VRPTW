from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import serializers, viewsets

from .models import Client, ClientDistance
from .serializers import ClientDistanceSerializer, ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by("id")
    serializer_class = ClientSerializer

    def create(self, request):
        response = super().create(request)
        if response.status_code == 201:
            creating_client = Client.objects.get(name=request.data["name"])
            for client, cost in request.data["cost"].items():
                client_distance_serializer = ClientDistanceSerializer(
                    data={
                        "client1": creating_client.name,
                        "client2": client,
                        "cost": cost,
                        "time": request.data["time"][client],
                    }
                )
                if client_distance_serializer.is_valid():
                    client_distance_serializer.save()

        return response

    def partial_update(self, request, pk):
        client_distance = ClientDistance.objects.filter(client1__id=pk).all()
        for client in client_distance:
            client_distance_serializer = ClientDistanceSerializer(
                client,
                data={
                    "cost": request.data["cost"][client.client2.name],
                    "time": request.data["time"][client.client2.name],
                },
                partial=True,
            )
            if client_distance_serializer.is_valid():
                client_distance_serializer.save()
        client_distance = ClientDistance.objects.filter(client2__id=pk).all()
        for client in client_distance:
            client_distance_serializer = ClientDistanceSerializer(
                client,
                data={
                    "cost": request.data["cost"][client.client1.name],
                    "time": request.data["time"][client.client1.name],
                },
                partial=True,
            )
            if client_distance_serializer.is_valid():
                client_distance_serializer.save()
        return super().partial_update(request, pk)


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))
