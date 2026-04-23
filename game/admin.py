from django.contrib import admin
from .models import Location, Catch, Order, Badge

admin.site.register(Location)
admin.site.register(Catch)
admin.site.register(Order)
admin.site.register(Badge)