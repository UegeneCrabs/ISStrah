# Generated by Django 4.2.6 on 2024-05-14 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casco', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='coefficient',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Коэффициент'),
        ),
    ]
