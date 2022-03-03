# Generated by Django 3.1.2 on 2021-06-08 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Art', '0002_auto_20210602_2106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='images',
            new_name='item_images',
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]