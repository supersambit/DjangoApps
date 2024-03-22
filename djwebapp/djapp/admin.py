from django.contrib import admin
from .models import CustomUser, Vehicle

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Vehicle)
