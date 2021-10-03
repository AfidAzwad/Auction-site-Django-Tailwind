# Generated by Django 3.1 on 2021-10-02 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebay', '0003_customer_cname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('a_id', models.AutoField(primary_key=True, serialize=False)),
                ('aname', models.CharField(max_length=50)),
                ('a_email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='products',
            name='owner',
        ),
    ]
