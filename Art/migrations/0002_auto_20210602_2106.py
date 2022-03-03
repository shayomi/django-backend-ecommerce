# Generated by Django 3.1.2 on 2021-06-02 20:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Art', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]