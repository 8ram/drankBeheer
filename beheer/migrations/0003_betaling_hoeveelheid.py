# Generated by Django 3.1.5 on 2021-01-04 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beheer', '0002_leider_volgorde'),
    ]

    operations = [
        migrations.AddField(
            model_name='betaling',
            name='hoeveelheid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
