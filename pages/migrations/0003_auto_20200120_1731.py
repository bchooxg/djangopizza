# Generated by Django 2.2.5 on 2020-01-20 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='postal_code',
            field=models.DecimalField(decimal_places=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='unit_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]