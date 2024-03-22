# Generated by Django 5.0.1 on 2024-01-24 17:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_number', models.CharField(max_length=12)),
                ('vehicle_type', models.CharField(choices=[('Stuff', 'Stuff'), ('Cycle', 'Cycle'), ('Bike', 'Bike'), ('Auto', 'Auto'), ('Car', 'Car')], max_length=10)),
                ('has_helmet', models.BooleanField()),
                ('entry_time', models.DateTimeField()),
                ('exit_time', models.DateTimeField(blank=True, null=True)),
                ('fare', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
