# Generated by Django 3.1.2 on 2021-06-10 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Art', '0005_item_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
