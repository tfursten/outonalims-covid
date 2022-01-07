# Generated by Django 3.1.2 on 2021-12-08 18:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0007_auto_20211204_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='booster_date',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='dose_1_date',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='dose_2_date',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='pneumococcal_date',
        ),
        migrations.AddField(
            model_name='subject',
            name='booster_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='booster_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1980)]),
        ),
        migrations.AddField(
            model_name='subject',
            name='dose_1_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='dose_1_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1980)]),
        ),
        migrations.AddField(
            model_name='subject',
            name='dose_2_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='dose_2_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1980)]),
        ),
        migrations.AddField(
            model_name='subject',
            name='pneumococcal_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1980)]),
        ),
    ]