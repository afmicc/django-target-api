# Generated by Django 3.0.7 on 2020-07-29 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0002_auto_20200723_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
    ]