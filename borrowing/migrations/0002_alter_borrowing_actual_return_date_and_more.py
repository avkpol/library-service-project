# Generated by Django 4.2.2 on 2023-06-10 17:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("borrowing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="actual_return_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="borrowing",
            name="expected_return_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]