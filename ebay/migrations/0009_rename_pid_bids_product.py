# Generated by Django 4.0 on 2022-01-26 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebay', '0008_bids'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='pid',
            new_name='product',
        ),
    ]
