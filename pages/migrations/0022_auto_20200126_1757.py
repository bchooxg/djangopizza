# Generated by Django 2.2.5 on 2020-01-26 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0021_auto_20200126_1615'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={},
        ),
        migrations.AlterModelOptions(
            name='order_status',
            options={'get_latest_by': ['id']},
        ),
        migrations.AlterField(
            model_name='order_status',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]