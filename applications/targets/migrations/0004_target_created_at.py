# Generated by Django 3.0.7 on 2020-08-25 20:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0003_auto_20200729_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]