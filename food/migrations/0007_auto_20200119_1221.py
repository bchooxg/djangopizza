# Generated by Django 2.2.5 on 2020-01-19 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_auto_20200119_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topping_count',
            name='amt',
            field=models.IntegerField(default=1),
        ),
    ]
