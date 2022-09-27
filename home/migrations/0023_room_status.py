# Generated by Django 4.1 on 2022-08-23 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_alter_order_date_of_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('available', 'Свободна'), ('taken', 'Занята')], default=('available', 'Свободна'), max_length=20),
        ),
    ]