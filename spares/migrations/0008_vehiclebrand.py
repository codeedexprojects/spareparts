# Generated by Django 3.2.10 on 2024-06-04 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0007_vehiclecategories'),
    ]

    operations = [
        migrations.CreateModel(
            name='vehicleBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicleBrands', models.CharField(max_length=100, null=True)),
                ('vehicle_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spares.vehiclecategories')),
            ],
        ),
    ]
