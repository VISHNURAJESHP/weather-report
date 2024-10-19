# Generated by Django 5.1.2 on 2024-10-19 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('alert_message', models.TextField()),
                ('triggered_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('avg_temp', models.FloatField()),
                ('max_temp', models.FloatField()),
                ('min_temp', models.FloatField()),
                ('dominant_condition', models.CharField(max_length=100)),
            ],
            options={
                'unique_together': {('city', 'date', 'time')},
            },
        ),
    ]
