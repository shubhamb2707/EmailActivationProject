# Generated by Django 2.2 on 2020-09-18 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmailApp', '0005_promo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Promo',
            new_name='Promo_codes',
        ),
    ]
