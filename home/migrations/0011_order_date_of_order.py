# Generated by Django 4.1 on 2022-08-23 11:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_order_date_of_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_of_order',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
