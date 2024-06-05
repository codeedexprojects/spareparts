# Generated by Django 3.2.10 on 2024-06-05 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0015_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partscategory',
            name='description',
        ),
        migrations.RemoveField(
            model_name='partscategory',
            name='part_image',
        ),
        migrations.RemoveField(
            model_name='partscategory',
            name='parts_Cat',
        ),
        migrations.RemoveField(
            model_name='partscategory',
            name='price',
        ),
        migrations.RemoveField(
            model_name='partscategory',
            name='v_brand',
        ),
        migrations.RemoveField(
            model_name='partscategory',
            name='v_category',
        ),
        migrations.AddField(
            model_name='partscategory',
            name='Parts_Categories',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
