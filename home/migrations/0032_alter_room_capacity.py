# Generated by Django 4.1 on 2022-09-10 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_alter_order_customer_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]
