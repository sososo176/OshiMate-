# Generated by Django 5.2.3 on 2025-06-25 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_itemlist_is_tutorial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
