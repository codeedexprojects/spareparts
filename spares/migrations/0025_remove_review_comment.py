# Generated by Django 3.2.10 on 2024-06-10 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0024_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='comment',
        ),
    ]
