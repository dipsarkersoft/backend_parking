# Generated by Django 5.1.4 on 2025-01-27 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price_p_h', models.IntegerField()),
                ('total_slots', models.IntegerField()),
                ('available_slots', models.IntegerField()),
            ],
        ),
    ]
