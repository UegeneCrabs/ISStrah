# Generated by Django 4.2.6 on 2024-05-18 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0006_alter_lifeinsurancerecord_competition_participation'),
    ]

    operations = [
        migrations.CreateModel(
            name='DamageThemeLife',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название тематики')),
            ],
            options={
                'verbose_name': 'Тема повреждения Жизнь',
                'verbose_name_plural': 'Темы повреждений Жизнь',
            },
        ),
        migrations.AddField(
            model_name='lifepayoutassessment',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='life.damagethemelife', verbose_name='Тематика повреждения'),
        ),
    ]
