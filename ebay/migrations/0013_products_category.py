# Generated by Django 4.0 on 2022-02-03 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ebay', '0012_category_alter_bids_bider_alter_bids_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='category',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='ebay.category'),
        ),
    ]