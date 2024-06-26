# Generated by Django 5.0.5 on 2024-06-10 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_api', '0004_alter_subscription_plan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporary',
            name='temp_duration',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='temporary',
            name='temp_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='temporary',
            name='temp_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='temporary',
            name='temp_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='temporary',
            name='temp_tenant_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
