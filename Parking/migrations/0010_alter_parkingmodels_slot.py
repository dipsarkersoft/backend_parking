# Generated by Django 5.1.4 on 2025-02-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parking', '0009_alter_parkingmodels_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingmodels',
            name='slot',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
