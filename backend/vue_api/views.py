from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import serializers, viewsets
from rest_framework.request import clone_request

from .models import Client, ClientDistance, Result
from .serializers import ClientDistanceSerializer, ClientSerializer, ResultClientSerializer, ResultSerializer


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


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all().order_by("id")
    serializer_class = ResultSerializer

    def create(self, request):
        request.data["user"] = request.user.pk

        print(request.data, flush=True)
        max_capacity = request.data["capacity"]
        cl_serv = request.data["clients"]
        odl = {}
        cost = {}
        for client in ["Depot", *cl_serv.keys()]:
            for client2 in ["Depot", *cl_serv.keys()]:
                if client != client2:
                    try:
                        client_distance = ClientDistance.objects.get(client1__name=client, client2__name=client2)
                    except ObjectDoesNotExist:
                        client_distance = ClientDistance.objects.get(client1__name=client2, client2__name=client)
                    odl[(client, client2)] = client_distance.time
                    cost[(client, client2)] = client_distance.cost
                    print(client, client2, client_distance, flush=True)
        print(odl, flush=True)
        print(cost, flush=True)
        return False

        response = super().create(request)
        if response.status_code == 201:
            creating_result = Result.objects.get(name=request.data["name"])
            for client, data in request.data["clients"].items():
                result_client_serializer = ResultClientSerializer(
                    data={
                        "result": creating_result.name,
                        "client": client,
                        "start": data["start"],
                        "end": data["end"],
                        "demand": data["demand"],
                    }
                )
                if result_client_serializer.is_valid():
                    result_client_serializer.save()

        return response


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))
