# Generated by Django 3.0.7 on 2020-08-24 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='', max_length=20, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('body', models.CharField(max_length=1000)),
            ],
        ),
    ]
