# Generated by Django 5.1.4 on 2025-01-27 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingmodels',
            name='end_park',
            field=models.DateTimeField(blank=True, default=0, null=True),
        ),
    ]
