# Generated by Django 3.1.2 on 2022-02-25 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0010_auto_20220221_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='week',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
