# Generated by Django 4.0 on 2021-12-30 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='newsletter',
            field=models.BooleanField(default=True),
        ),
    ]
