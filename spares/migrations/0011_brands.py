# Generated by Django 3.2.10 on 2024-06-04 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0010_vehiclecategories'),
    ]

    operations = [
        migrations.CreateModel(
            name='brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_Brand', models.CharField(max_length=100, null=True)),
                ('vehicle_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spares.vehiclecategories')),
            ],
        ),
    ]