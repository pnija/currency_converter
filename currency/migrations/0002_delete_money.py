# Generated by Django 2.1.4 on 2018-12-27 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Money',
        ),
    ]