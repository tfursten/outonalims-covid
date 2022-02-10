# Generated by Django 3.1.2 on 2022-01-14 22:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0008_auto_20211208_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='fifth_covid_case_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='fifth_covid_case_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1980)]),
        ),
        migrations.AddField(
            model_name='subject',
            name='first_covid_case_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='first_covid_case_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1980)]),
        ),
        migrations.AddField(
            model_name='subject',
            name='fourth_covid_case_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='fourth_covid_case_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1980)]),
        ),
        migrations.AddField(
            model_name='subject',
            name='second_covid_case_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='second_covid_case_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1980)]),
        ),
        migrations.AddField(
            model_name='subject',
            name='third_covid_case_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='third_covid_case_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1980)]),
        ),
    ]