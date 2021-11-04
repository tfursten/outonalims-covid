# Generated by Django 3.1.2 on 2021-10-27 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0005_pool'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pool',
            name='storage_location',
        ),
        migrations.AddField(
            model_name='pool',
            name='box',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lims.box'),
        ),
        migrations.AddField(
            model_name='pool',
            name='box_position',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pool',
            name='name',
            field=models.CharField(default='pool', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
