# Generated by Django 5.1.4 on 2025-02-01 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='available_slots_list',
            field=models.JSONField(default=list),
        ),
    ]
