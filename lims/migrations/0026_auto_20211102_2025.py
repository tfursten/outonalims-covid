# Generated by Django 3.1.2 on 2021-11-03 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0025_auto_20211102_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='rep',
        ),
        migrations.AddField(
            model_name='testresult',
            name='name',
            field=models.CharField(default='result', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
