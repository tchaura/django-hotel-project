# Generated by Django 4.1 on 2022-08-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_remove_room_id_alter_room_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
