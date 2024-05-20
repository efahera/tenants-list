# Generated by Django 5.0.5 on 2024-05-16 02:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('plan', models.CharField(choices=[('A', 'Plan A'), ('B', 'Plan B'), ('C', 'Plan C')], max_length=1, primary_key=True, serialize=False)),
                ('duration', models.CharField(blank=True, max_length=20, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('date_of_birth', models.DateField()),
                ('contact_number', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='tenant_images/')),
                ('plan_subscription', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo_api.subscription')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo_api.tenant')),
            ],
        ),
    ]