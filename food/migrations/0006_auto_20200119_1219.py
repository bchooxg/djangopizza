# Generated by Django 2.2.5 on 2020-01-19 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_topping_amt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topping',
            name='amt',
        ),
        migrations.AddField(
            model_name='topping_count',
            name='amt',
            field=models.IntegerField(null=True),
        ),
    ]
