# Generated by Django 4.1 on 2022-08-23 10:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_order_date_of_order_alter_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7b62dc5e-4796-4408-a1ed-0489507cfeb0'), primary_key=True, serialize=False),
        ),
    ]