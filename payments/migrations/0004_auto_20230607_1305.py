# Generated by Django 3.2.19 on 2023-06-07 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20230607_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='session_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='session_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
