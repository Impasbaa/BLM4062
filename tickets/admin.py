from django.contrib import admin
from .models import City, Bus, Trip, Ticket

# Modelleri admin paneline kaydediyoruz
admin.site.register(City)
admin.site.register(Bus)
admin.site.register(Trip)
admin.site.register(Ticket)