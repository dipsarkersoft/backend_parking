# Generated by Django 5.1.4 on 2025-02-01 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_categorymodel_available_slots_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='available_slots_list',
            field=models.JSONField(default=dict),
        ),
    ]
