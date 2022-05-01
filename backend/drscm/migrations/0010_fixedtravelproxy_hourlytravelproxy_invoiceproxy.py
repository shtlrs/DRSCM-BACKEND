# Generated by Django 3.2.13 on 2022-04-28 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("drscm", "0009_remove_project_hourly_rate"),
    ]

    operations = [
        migrations.CreateModel(
            name="FixedTravelProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("drscm.fixedtravel",),
        ),
        migrations.CreateModel(
            name="HourlyTravelProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("drscm.hourlytravel",),
        ),
        migrations.CreateModel(
            name="InvoiceProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("drscm.invoice",),
        ),
    ]
