# Generated by Django 3.0.7 on 2020-07-27 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200623_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='users/pictures'),
        ),
    ]
