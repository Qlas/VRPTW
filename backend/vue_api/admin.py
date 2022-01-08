from django.contrib import admin

from .models import Client, ClientDistance, Result, ResultClient

admin.site.register(Client)
admin.site.register(ClientDistance)
admin.site.register(Result)
admin.site.register(ResultClient)
