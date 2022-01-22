# Generated by Django 4.0 on 2022-01-22 13:51

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_newsletter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='newsletter',
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address_1', models.CharField(max_length=80)),
                ('street_address_2', models.CharField(blank=True, max_length=80, null=True)),
                ('town_or_city', models.CharField(max_length=40)),
                ('county', models.CharField(max_length=40)),
                ('postcode', models.CharField(max_length=20)),
                ('country', django_countries.fields.CountryField(default='IE', max_length=2)),
                ('phone_number', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='accounts.account')),
            ],
        ),
    ]