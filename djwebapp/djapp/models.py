from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.conf import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_user_permissions')


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('Stuff', 'Stuff'),
        ('Cycle', 'Cycle'),
        ('Bike', 'Bike'),
        ('Auto', 'Auto'),
        ('Car', 'Car'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=12)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    has_helmet = models.BooleanField()
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.vehicle_number
