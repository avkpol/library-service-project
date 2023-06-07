# Generated by Django 3.2.19 on 2023-06-07 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20230607_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELED', 'Canceled')], default='PENDING', max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='type',
            field=models.CharField(choices=[('CARD', 'Card'), ('CASH', 'Cash')], max_length=10),
        ),
    ]
