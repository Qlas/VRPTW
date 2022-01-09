from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import serializers, viewsets
from rest_framework.request import clone_request
from rest_framework.response import Response

from backend.algorithm.error import TWerror, client_capacity_error
from backend.algorithm.main_al import run_VRTW_algorithm

from .models import Client, ClientDistance, GlobalValues, Result
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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(
            queryset,
            many=True,
        )
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request):
        request.data["user"] = request.user.pk

        print(request.data, flush=True)
        max_capacity = request.data["capacity"]
        cl_serv = {"Depot": {"start": 0, "end": 0, "demand": 0}, **request.data["clients"]}
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
        print(cl_serv, flush=True)
        print(max_capacity, flush=True)
        print(odl, flush=True)
        print(cost, flush=True)
        print("aaa")
        global_values = GlobalValues.objects.first()
        try:
            algorithm_result = run_VRTW_algorithm(
                cl_serv, max_capacity, odl, cost, global_values.tabu_term, global_values.maxint
            )
        except (client_capacity_error, TWerror) as e:
            return Response({str(e): e.args}, status=400)
        print(algorithm_result, flush=True)
        request.data["cost"] = algorithm_result[1]
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
                        "truck": algorithm_result[0][client][0],
                        "position": algorithm_result[0][client][1],
                        "start_of_service": algorithm_result[2][client],
                    }
                )
                if result_client_serializer.is_valid():
                    result_client_serializer.save()

        return response


class ClientDistanceViewSet(viewsets.ModelViewSet):
    queryset = ClientDistance.objects.all().order_by("id")
    serializer_class = ClientDistanceSerializer


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))
