# Generated by Django 4.1 on 2022-08-23 12:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_alter_order_date_of_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_of_order',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 12, 0, 47, 731935, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
