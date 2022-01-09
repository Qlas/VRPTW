from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import DateTimeField, ExpressionWrapper, F, Q


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class ClientDistance(models.Model):
    client1 = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client1")
    client2 = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client2")
    cost = models.FloatField()
    time = models.FloatField()

    def __str__(self) -> str:
        return f"{self.client1} - {self.client2} - {self.cost} - {self.time}"


class Result(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, related_name="results", on_delete=models.SET_NULL, blank=True, null=True)
    capacity = models.IntegerField()
    cost = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}, {self.user}, {self.cost}"


class ResultClient(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="result_client")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start = models.FloatField()
    end = models.FloatField()
    demand = models.FloatField()
    truck = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.result.name} - {self.client.name} - {self.truck} - {self.position}"


class GlobalValues(models.Model):
    cad = models.IntegerField()
    maxint = models.IntegerField()
