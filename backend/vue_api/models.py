from django.contrib.auth.models import User
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
    cost = models.IntegerField()
    time = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.client1} - {self.client2} - {self.cost} - {self.time}"
