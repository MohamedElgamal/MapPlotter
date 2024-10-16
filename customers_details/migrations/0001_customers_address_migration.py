# Generated by Django 5.1.1 on 2024-10-13 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(default='', max_length=256)),
                ('customer_created_at', models.DateTimeField(auto_now_add=True)),
                ('customer_updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'customers',
            },
        ),
        migrations.CreateModel(
            name='OsmAddresses',
            fields=[
                ('osm_address_id', models.AutoField(primary_key=True, serialize=False)),
                ('osm_geo_location', models.JSONField()),
                ('osm_created_at', models.DateTimeField(auto_now_add=True)),
                ('osm_updated_at', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='osm_addresses', to='customers_details.customers')),
            ],
            options={
                'db_table': 'osm_addresses',
            },
        ),
        migrations.CreateModel(
            name='OsoulCustomersDetails',
            fields=[
                ('osoul_person_id', models.AutoField(primary_key=True, serialize=False)),
                ('osoul_account_num', models.IntegerField(default=0)),
                ('osoul_person_code', models.IntegerField()),
                ('osoul_address', models.CharField(default='', max_length=512)),
                ('osoul_person_created_at', models.DateTimeField(auto_now_add=True)),
                ('osoul_person_updated_at', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='osoul', to='customers_details.customers')),
            ],
            options={
                'db_table': 'osoul_customers_details',
            },
        ),
        migrations.CreateModel(
            name='CustomerPhones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_num', models.CharField(default='', max_length=25)),
                ('phone_created_at', models.DateTimeField(auto_now_add=True)),
                ('phone_updated_at', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='customers_details.customers')),
            ],
            options={
                'db_table': 'customer_phones',
                'unique_together': {('phone_num', 'customer')},
            },
        ),
    ]
